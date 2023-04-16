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

class DataLoader(object):
    def __init__(self, filename):
        self.filename = filename
        self.data = CSVReader(filename)
        self.tags = self.data.get_all_tags()
        self.img_dir = os.path.join(os.getcwd(), 'images')
        # self.img_files = os.listdir(self.img_dir)
        # self.img_list = [img for img in self.img_files if img.endswith(".jpg")]
        # self.img_path = os.path.join(self.img_dir, self.img_list[0])
        self.ng = NoiseGenerator()

    def get_params(self, tag):
        row = self.data.get_row(tag)
        location = row['LatLong']
        fov = row['FOV']
        heading = row['Heading']
        pitch = row['Pitch']
        return location, fov, heading, pitch

    def get_image(self, tag, api_key, image_tag=None, fov=None, heading=None, pitch=None):
        if image_tag == None:
            image_tag = tag
        location = self.get_params(tag)[0]
        if fov == None:
            fov = self.get_params(tag)[1]
        if heading == None:
            heading = self.get_params(tag)[2]
        if pitch == None:
            pitch = self.get_params(tag)[3]
        sv = StreetViewer(api_key=api_key, location=location, fov=fov, heading=heading, pitch=pitch, verbose=True, tag=image_tag)
        sv.get_meta()
        sv.get_pic()

    def get_image_batch(self, tag, api_key):
        tag_counter = 1
        location, fov, heading, pitch = self.get_params(tag)
        self.get_image(tag, api_key, image_tag=tag)
        # This is for the actual number of images (81)
        # for i in range (-4, 5):
        #     for j in range (-4, 5):
        # Right now we are using this for testing purposes (9)
        for i in range (-1, 2):
            for j in range (-1, 2):
                if i == 0 and j == 0:
                    continue
                self.get_image(tag, api_key, image_tag=tag + "-" +str(tag_counter), fov=fov + max(i, j), heading=heading + i, pitch=pitch + j)
                tag_counter += 1
    

# # Run the following code to test the data_loader.py file:
# load_dotenv()
# dl = DataLoader('uoft_locations.csv')
# dl.get_image_batch('JO_2678', os.getenv('API_KEY'))