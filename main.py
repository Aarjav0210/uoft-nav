
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#Get access to functions from streetview.py
from street_viewer import StreetViewer
#for csv file
import pandas as pd
import os
from dotenv import load_dotenv
from csv_reader import CSVReader
from noise_generator import NoiseGenerator
from data_loader import DataLoader
from resnet2 import ResNet2


from tensorflow.keras.layers import Conv2D, Flatten, Dense, MaxPool2D, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.applications.resnet34 import ResNet34, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.keras.models import Sequential, Model

import numpy as np

import splitfolders


# #load API key
# load_dotenv()

# #load data from csv file
# filename = 'uoft_locations.csv'
# uoft_data = CSVReader(filename)

# #Get image -- uses API calls, so only run when necessary
# # uoft_tags = uoft_data.get_all_tags()
# # uoft_data.get_image(uoft_tags[25], os.getenv('API_KEY'))

# img_dir = os.path.join(os.getcwd(), 'images')
# img_files = os.listdir(img_dir)
# img_list = [img for img in img_files if img.endswith(".jpg")]
# img_path = os.path.join(img_dir, img_list[0])

# # ng = NoiseGenerator()
# # ng.show_noise(img_path, 'low')
# # ng.show_noise(img_path, 'high')

load_dotenv()
dl = DataLoader('uoft_locations.csv')
building_tags = dl.tags
for tag in building_tags:
    img_list = dl.get_image_batch(tag, os.getenv('API_KEY'), noise=True)
    dl.save_image_batch(img_list)

net = ResNet2()
net.run()