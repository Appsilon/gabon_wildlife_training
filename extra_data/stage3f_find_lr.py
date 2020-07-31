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
learn.load(PATH_TO_MODELS / "stage2f-5epochs-384_512-rescaled");

learn.freeze()

run_find_lr(learn, "stage3f-5epochs-576_768-rescaled")

# lr = 1e-3
# n_epochs = 5

# run_training(learn, "stage1f-5epochs-384_512-rescaled", lr=lr, n_epochs=n_epochs)

# fig = learn.recorder.plot_losses(return_fig=True)
# fig.savefig("loss_plot-stage1f-5epochs-384_512-rescaled.png")

# # learn = get_initial_learner(data)
# # learn.load(PATH_TO_MODELS / "stage1f-5epochs-384_512-rescaled");

# interp = ClassificationInterpretation.from_learner(learn)

# # interp.plot_confusion_matrix(figsize=(12,12), dpi=60)

# conf_m = interp.confusion_matrix()
# np.save("conf_m-stage1f-5epochs-384_512-rescaled.npy", conf_m)

# correct_p = sum([conf_m[i,i] for i in range(len(conf_m))])
# all_p = conf_m.sum().sum()
# print(f"accuracy is: {round(100 * correct_p / all_p,2)}%")

# plot_conf_matrix_reordered(conf_m,
#                            sorted(classes),
#                            save_as = "conf_m-new_order-stage1f-5epochs-384_512-rescaled.png", 
#                            for_model = "stage1f-5epochs-384_512-rescaled")