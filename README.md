This repo contains records of the modelling phase of the Gabon Wildlife MVP project.

# Links to key artifacts
* the best trained model
* the best trained model using only rescaled (~384x512) images
* the train/test split used for training train_valid_df.csv
* csv with all data (???)
* all exif data collected so far
* the images of disks with full data and rescaled data
* notes on training runs with links to Weights&Biases
* csv with raw labels from Robbie Whytock

# Key findings
1. images come in sequences (e.g., 30 images long), one can identify them using algorithmic methods or with datetimes
2. images come from many sources with varying species distributions
3. images have varying sizes, from 1088x816 to 3264x2448

# Process description and contents

## data_dive
* extraction of datetimes from EXIFs - not utilized yet
* identifying sequences algorithmically by
  * hashing
  * histogram comparisons
  * NN feature extraction + k-means clustering
* inspect image dimensions and rescale images

## inspect_data_split_validation
* missing images (8)
* inspect of metadata from Robbie Whytock (source-path-datetime), see inspect_data_04_investigate_metadata_from_Robbie.ipynb
* train/test split and data summary inspect_data_05_validation_split_on_subfolders.ipynb
* inspect sizes of images based on exif inspect_data_06_find_images_sizes.ipynb

## training

## inspect_model
