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
#rand
import random

class DataLoader(object):
    def __init__(self, filename):
        self.filename = filename
        self.data = CSVReader(filename)
        self.tags = self.data.get_all_tags()
        self.img_dir = os.path.join(os.getcwd(), './images/')
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

    def get_image(self, tag, api_key, fov=None, heading=None, pitch=None):#image_tag=None, fov=None, heading=None, pitch=None):
        # if image_tag == None:
        #     image_tag = tag
        location = self.get_params(tag)[0]
        if fov == None:
            fov = self.get_params(tag)[1]
        if heading == None:
            heading = self.get_params(tag)[2]
        if pitch == None:
            pitch = self.get_params(tag)[3]
        sv = StreetViewer(api_key=api_key, location=location, fov=fov, heading=heading, pitch=pitch, verbose=True, tag=tag)
        sv.get_meta()
        return (sv.get_pic(), tag)

    def get_image_batch(self, tag, api_key, noise=False):
        tag_counter = 1
        location, fov, heading, pitch = self.get_params(tag)
        # self.get_image(tag, api_key, image_tag=tag)
        # This is for the actual number of images (81)
        # for i in range (-4, 5):
        #     for j in range (-4, 5):
        # Right now we are using this for testing purposes (9)
        img_list = []
        for i in range (-1, 2):
            for j in range (-1, 2):
                # if i == 0 and j == 0:
                #     continue
                img = self.get_image(tag, api_key, fov=fov + max(i, j), heading=heading + i, pitch=pitch + j)[0] #image_tag=tag + "-" +str(tag_counter), fov=fov + max(i, j), heading=heading + i, pitch=pitch + j)
                if noise:
                    if random.randint(0, 1) == 1:
                        if random.randint(0, 1) == 1:
                            img = self.ng.generate_noise(img, 'low')
                        else:
                            img = self.ng.generate_noise(img, 'high')
                img_list.append((img, tag + "-" +str(tag_counter)))
                tag_counter += 1
        return img_list
    
    def save_image(self, image_content, tag, verbose=True):
        """
        Method to save StreetView image to local directory
        """
        if image_content is not None:
            self.pic_path = "{}pic_{}.jpg".format(
                self.img_dir, tag)
            # self.pic_path = "{}pic_{}.jpg".format(
            #     self.folder_directory, "test")
            with open(self.pic_path, 'wb') as file:
                file.write(image_content)
            if verbose:
                print(f">>> Image saved to {self.pic_path}")
        else:
            print(">>> No image content available, cannot save image!")
    
    def save_image_batch(self, img_list, verbose=True):
        for img in img_list:
            self.save_image(img[0], img[1], verbose)

    
    
    

# # Run the following code to test the data_loader.py file:
load_dotenv()
dl = DataLoader('uoft_locations.csv')
img_list = dl.get_image_batch('BA_3348', os.getenv('API_KEY'), noise=True)
dl.save_image_batch(img_list)

# for img in dl.get_image_batch('JO_2678', os.getenv('API_KEY')):
#     dl.save_image(img[0], img[1])