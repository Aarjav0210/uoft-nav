
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

#load API key
load_dotenv()

#load data from csv file
filename = 'uoft_locations.csv'
uoft_data = CSVReader(filename)

#Get image -- uses API calls, so only run when necessary
# uoft_tags = uoft_data.get_all_tags()
# uoft_data.get_image(uoft_tags[25], os.getenv('API_KEY'))

img_dir = os.path.join(os.getcwd(), 'images')
img_files = os.listdir(img_dir)
img_list = [img for img in img_files if img.endswith(".jpg")]
img_path = os.path.join(img_dir, img_list[0])

# ng = NoiseGenerator()
# ng.show_noise(img_path, 'low')
# ng.show_noise(img_path, 'high')