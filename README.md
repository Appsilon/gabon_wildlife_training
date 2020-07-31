This repo contains records of the modelling phase of the Gabon Wildlife MVP project - the model is used in the MVP of Mbaza AI.

# Links to key artifacts
* [the best trained model](https://github.com/Appsilon/gabon_wildlife_training/releases/tag/v1.0-model)
* [the train/test split used for training train_valid_df.csv](https://github.com/Appsilon/gabon_wildlife_training/releases/tag/v1.0-train_valid_df)
* [all exif datetimes collected so far](https://github.com/Appsilon/gabon_wildlife_training/tree/master/data_dive/datetimes_exif)
* the snapshots of disks with [full data](https://console.cloud.google.com/compute/snapshotsDetail/projects/wildlifeexplorer/global/snapshots/snapshot-wildlife-explorer-data?project=wildlifeexplorer) and [rescaled data](https://console.cloud.google.com/compute/snapshotsDetail/projects/wildlifeexplorer/global/snapshots/snapshot-wildlife-explorer-data-rescaled?project=wildlifeexplorer) (restricted access)
* [notes on training runs with links to Weights&Biases](https://github.com/Appsilon/gabon_wildlife_training/blob/master/notes_on_training_runs.md)
* [csv with raw labels from Robbie Whytock](https://github.com/Appsilon/gabon_wildlife_training/releases/tag/v1.0-raw_csv)

# Key findings
1. images come in sequences (e.g., 30 images long), one can identify them using algorithmic methods or with datetimes
2. images come from many sources with varying species distributions
3. images have varying sizes, from 1088x816 to 3264x2448 and proportions, form 1.25 to 1.78
4. had issues with Neptune reporting (on/off of callbacks) - switched to Weights&Biases
5. training worked best when training on 384x512 -> 576x768 images (starting lower seemed to overfit quickly, probably due to sequence redundancy)
6. best model has **accuracy 80%**, top2_accuracy = 88.97%, top3_accuracy = 92.15%
7. accuracies vary significantly per source and per species
8. grad-CAM suggests the right parts of images are used for inference
9. extra data on gorillas and chimps plus removing some mislabels, helped accuracy on gorillas and chimps, but overall the accuracy stayed similar

# Process description and contents

## data_dive
* extraction of datetimes from EXIFs - not utilized yet
* identifying sequences algorithmically by
  * hashing
  * histogram comparisons
  * NN feature extraction + k-means clustering
* inspect image sizes and rescale images

## inspect_data_split_validation
* missing images (8)
* inspect of metadata from Robbie Whytock (source-path-datetime), see inspect_data_04_investigate_metadata_from_Robbie.ipynb
* train/test split and data summary inspect_data_05_validation_split_on_subfolders.ipynb
* inspect sizes of images based on exif inspect_data_06_find_images_sizes.ipynb (we used method from data_dive eventually)

## training
* started with reporting in Neptune, but due to issues with callbacks, turned to Weights&Biases
* [notes on training runs with links can be found here](https://github.com/Appsilon/gabon_wildlife_training/blob/master/notes_on_training_runs.md)
* functions used during training are in functions_wandb.py and functions_wandb_no_rescale.py (depending on the data used)
* best model was trained first on 384x512 images (stage1a and stage2a - training_13_wandb_full_from_scratch_bigger_images.ipynb) next on 576x768 images (stage3a and stage4a - training_14_wandb_full_from_scratch_bigger_images.ipynb)
* **best model has accuracy of 80%**
* confusion matrix for best model with grouped species (conf_m-new_order-stage4a-5epochs-576_768-rescaled.png)
* accuracy of best model on rescaled validation set is 76% (training_15-check_4a_on_rescaled.ipynb)

## inspect_model
* top2 and top3 accuracies of best model (inspect_model_02.ipynb)
* accuracies per species vary significantly (inspect_model_02.ipynb)
* accuracies per source vary significantly (Compressed Camera Trap Images > Camera trap Nki National Park > allData) (inspect_model_02.ipynb)
* plots of confusion matrices for a subset of data (e.g., per source) (inspect_model_03.ipynb)
* use grad-CAM ideas to inspect areas of images used for making predictions (inspect_model_4a...)

## extra_data
* added some extra chimp and gorilla images, removed some mislabels (train_valid_df_200722.csv contains the new data list)
* retrained the model with to_fp16()
* tried EfficientNet but training was super slow, so stuck to ResNet50
* improved on chimps and gorillas noticeably, however, overall the accuracy was slightly lower ([release with model](https://github.com/Appsilon/gabon_wildlife_training/releases/tag/v1.0-model-extra-data))

# Ideas for future improvements
* use Megadetector to detect animal, then classify it
* possibly ensamble the above model with the current one
* remove Blank and use sigmoid activation full argument starts from 45:00 of https://course.fast.ai/videos/?lesson=10
* rescale all the data - not just current train+valid (in case useful)
* ~~use .to_fp16() (reduce precision to speed up and help generalization)~~
* use ResNeXt architecture
* investigate day vs night performance of models (bare in mind some day images are B&W)
* investigate label quality - are Bird and Rail_Nkulengu disjoint? Are Monkey and Mandrillus disjoint? Are primates classified correctly? Are the 650 Rat_Giant in allData/StephBrittainZSL really there?
