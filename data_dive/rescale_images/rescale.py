from pathlib import Path
import os
import piexif
import numpy as np

from tqdm.notebook import tqdm
from PIL import Image

from joblib import Parallel, delayed

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


PATH_TO_IMG = Path("/data/Gabon_trainingData")

# PATH_TO_MAIN = Path("/home/jupyter/")
# PATH_TO_TRAIN_DF = PATH_TO_MAIN / "inspect_data_split_validation"

PATH_TO_IMG_RESC = Path("/data_rescaled/")


filename_sizes = "sizes.npy"
sizes_from_file = np.load(filename_sizes).tolist()  # x, y, image

x_y_image = sizes_from_file

exceptions = []
for x_y_image in tqdm(x_y_image):
    try:
        filename = x_y_image[2]
        new_filename = "resc_" + filename
        if os.path.isfile(PATH_TO_IMG_RESC / new_filename):
            continue
        img = Image.open(PATH_TO_IMG / filename)
        y = 384
        scale = 384 / int(x_y_image[1])
        x = round(scale * int(x_y_image[0]))
        img = img.resize((x, y), Image.ANTIALIAS)
        img.save(PATH_TO_IMG_RESC / new_filename)
        piexif.transplant(PATH_TO_IMG / filename, PATH_TO_IMG_RESC / new_filename)
    except Exception as e:
        exceptions.append([x_y_image, e])
        
np.save("exceptions.npy", exceptions)