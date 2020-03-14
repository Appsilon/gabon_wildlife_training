from pathlib import Path
import json
import logging

import numpy as np
import pandas as pd

from fastai.vision import *

import os

# import neptune
# from neptunecontrib.monitoring.fastai import NeptuneMonitor
import wandb
from wandb.fastai import WandbCallback

import configparser

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import matplotlib.pyplot as plt
import seaborn as sns

####################################################################

PATH_TO_IMG = Path("/data_rescaled")

PATH_TO_MAIN = Path("/home/jupyter/")
PATH_TO_TRAIN_DF = PATH_TO_MAIN / "inspect_data_split_validation"
PATH_TO_MODELS = PATH_TO_MAIN / "training" / "saved_models"
PATH_TO_CONFIG = PATH_TO_MAIN / "config"

# CONFIG = configparser.ConfigParser()
# CONFIG.read(PATH_TO_CONFIG / "neptune.ini")

####################################################################

def get_training_data(df, img_size, batch_size=512, partial_pct=1.0):
    np.random.seed(273)
    src = (ImageList.from_df(df, cols="uniqueName", path=PATH_TO_IMG)
           .use_partial_data(partial_pct)
           .split_from_df("is_valid")
           .label_from_df(cols="species"))

    tfms = get_transforms()  # TODO
    data = (src.transform(tfms, size=img_size, padding_mode ="zeros")
            .databunch(bs=batch_size).normalize(imagenet_stats))
    return data

def get_initial_learner(data):
#     acc_02 = partial(accuracy_thresh, thresh=0.2)
    learn = cnn_learner(data, models.resnet50, metrics=[accuracy], callback_fns=[partial(WandbCallback)])
    learn.model_dir = PATH_TO_MODELS
    return learn

def save_model(learn, name):
    """ This function saves the model in 'learn' to a file 'name',
    however, it saves a version stripped of callbacks (e.g., wandb) as it spoil
    inference when wandb is not available, preserving it in learn.
    """
    callback_fns = learn.callback_fns  # preserve wandb callback and others 
    learn.callback_fns = []  # clean callbacks
    
    learn.save(PATH_TO_MODELS / name)  # save only weights, adds .pth automatically
    learn.export(PATH_TO_MODELS / f"{name}.pkl")  # serialize entire model, need to add .pkl

    learn.callback_fns = callback_fns  # restore callbacks
    
def load_weights(learn, name):
    if (PATH_TO_MODELS / f"{name}.pth").is_file():
        learn.load(PATH_TO_MODELS / name)
        return True
    else:
        return False

def run_training(learn, model_name, lr, n_epochs, lr_end=None):
    if load_weights(learn, model_name):
        logging.info(f"Loaded weights for {model_name}, skipping training")
    else:
        logging.info(f"running training {model_name}")
        
        wandb.config[f"{model_name}_lr"] = lr
        wandb.config[f"{model_name}_n_epochs"] = n_epochs

        lr_slice = slice(lr)
        if lr_end:
            wandb.config[f"{model_name}_lr_end"] = lr_end
            lr_slice = slice(lr, lr_end)

        learn.fit_one_cycle(n_epochs, lr_slice)
        logging.info(f"finished training {model_name}")
        save_model(learn, model_name)
        logging.info(f"saved {model_name}")
        
def run_find_lr(learn, model_name):
    learn.lr_find()
    fig = learn.recorder.plot(return_fig=True)
    fig_name = f"lr_find_for_{model_name}"
    fig.savefig(fig_name + ".png")
    wandb.log({fig_name: fig})

def plot_conf_matrix_reordered(conf_m, old_order, new_order, for_model=None, save_as=None):
    df_conf_m = pd.DataFrame(conf_m, index=old_order, columns=old_order)
    
    new_df_conf_m = df_conf_m.copy()
    new_df_conf_m.columns = new_order
    new_df_conf_m.index = new_order
    
    for i_species in new_order:
        for j_species in new_order:
            new_df_conf_m.loc[i_species, j_species] = df_conf_m.loc[i_species, j_species]
    
    plt.figure(figsize = (12,12))
    ax = sns.heatmap(new_df_conf_m, annot=True, cmap=sns.color_palette("Blues", n_colors=10), cbar=False, fmt="d")
    bottom, top = ax.get_ylim()
    ax.set_ylim(bottom + 0.5, top - 0.5)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    
    plt.title("Confusion matrix")
    if for_model:
        plt.title(f"Confusion matrix for model {for_model}")
    
    plt.tight_layout()
        
    if save_as:
        plt.savefig(save_as)

# wandb.init(project="gabon")