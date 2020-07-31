from pathlib import Path
import json
import logging

import numpy as np
import pandas as pd

from fastai.vision import *

import os

import wandb
from wandb.fastai import WandbCallback

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import configparser

from functions_wandb_no_rescale import *


wandb.init(project="gabon")

df = pd.read_csv("../gabon_extra_data/train_valid_df_200722.csv")
classes = df.species.unique()

# df["uniqueName"] = df.uniqueName.apply(lambda x: "resc_" + x)

data = get_training_data(df, (576, 768), batch_size=32)#, partial_pct=0.01)

learn = get_initial_learner(data)
learn.load(PATH_TO_MODELS / "stage3f-5epochs-576_768-rescaled");

learn.unfreeze()

# run_find_lr(learn, "stage1f-5epochs-384_512-rescaled")

lr = 1e-6
lr_end = 1e-4/10
n_epochs = 8

run_training(learn, "stage4f-5epochs-576_768-rescaled", lr=lr, lr_end=lr_end, n_epochs=n_epochs)

fig = learn.recorder.plot_losses(return_fig=True)
fig.savefig("loss_plot-stage4f-5epochs-576_768-rescaled.png")

# learn = get_initial_learner(data)
# learn.load(PATH_TO_MODELS / "stage1f-5epochs-384_512-rescaled");

interp = ClassificationInterpretation.from_learner(learn)

# interp.plot_confusion_matrix(figsize=(12,12), dpi=60)

conf_m = interp.confusion_matrix()
np.save("conf_m-stage4f-5epochs-576_768-rescaled.npy", conf_m)

correct_p = sum([conf_m[i,i] for i in range(len(conf_m))])
all_p = conf_m.sum().sum()
print(f"accuracy is: {round(100 * correct_p / all_p,2)}%")
