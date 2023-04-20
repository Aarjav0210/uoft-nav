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
    def __init__(self, filename, api_key):
        self.filename = filename
        self.data = CSVReader(filename)
        self.tags = self.data.get_all_tags()
        self.img_dir = os.path.join(os.getcwd(), './images/')
        self.api_key = api_key
        self.ng = NoiseGenerator()

    # get params from csv file
    def get_params(self, tag):
        row = self.data.get_row(tag)
        location = row['LatLong']
        fov = row['FOV']
        heading = row['Heading']
        pitch = row['Pitch']
        return location, fov, heading, pitch
    
    # get image from streetview.py
    def get_image(self, tag, api_key, fov=None, heading=None, pitch=None):
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

    # get image batch from streetview.py with varying fov, heading, pitch
    # noise is a boolean that determines whether or not to add noise to random images
    def get_image_batch(self, tag, api_key, noise=False):
        location, fov, heading, pitch = self.get_params(tag)
        img_list = []
        for i in range (-8, 10, 2): ##horizontal axis for heading
            for j in range (-8, 10, 2): ##vertical axis for pitch 
                img = self.get_image(tag, api_key, fov=fov + ((i*j)/max(1,min(abs(i), abs(j)))), heading=heading + i, pitch=pitch + j)[0] #image_tag=tag + "-" +str(tag_counter), fov=fov + max(i, j), heading=heading + i, pitch=pitch + j)
                if noise:
                    if random.randint(0, 1) == 1:
                        if random.randint(0, 1) == 1:
                            img = self.ng.generate_noise(img, 'low')
                        else:
                            img = self.ng.generate_noise(img, 'high')
                img_list.append((img, tag))
        return img_list
    
    # save image in an image-specific folder to local directory
    def save_image(self, image_content, folder_tag, tag, verbose=True):
        """
        Method to save StreetView image to local directory
        """
        self.building_dir = os.path.join(self.img_dir, folder_tag)
        if not os.path.exists(self.building_dir):
            os.makedirs(self.building_dir)
        if image_content is not None:
            self.pic_path = os.path.join(self.building_dir, f"pic_{tag}.jpg")
            with open(self.pic_path, 'wb') as file:
                file.write(image_content)
            if verbose:
                print(f">>> Image saved to {self.pic_path}")
        else:
            print(">>> No image content available, cannot save image!")
    
    # save image batch in an image-specific folder to local directory
    def save_image_batch(self, img_list, verbose=True):
        for i, img in enumerate(img_list):
            self.save_image(img[0], img[1], img[1] + "-" + str(i), verbose)

    # save images to local directory
    def save_image1(self, image_content, target, tag, verbose=True):
        """
        Method to save StreetView image to local directory
        """
        if image_content is not None:
            self.pic_path = os.path.join(self.img_dir, f"{tag}.jpg")
            with open(self.pic_path, 'wb') as file:
                file.write(image_content)
            if verbose:
                print(f">>> Image saved to {self.pic_path}")
        else:
            print(">>> No image content available, cannot save image!")

    # save image batch to local directory
    def save_image_batch1(self, img_list, verbose=True):
        for i, img in enumerate(img_list):
            self.save_image1(img[0], img[1], img[1] + "-" + str(i), verbose)

    # save all images to local directory
    def save_all_images(self):
        for tag in self.tags[94:]:
            img_list = self.get_image_batch(tag, os.getenv('API_KEY'), noise=True)
            self.save_image_batch1(img_list)

    
    #load all classes from the csv
    def load_classes(self):
        classes = []
        for tag in self.tags:
            img_list = self.get_image_batch(tag, os.getenv('API_KEY'))
            classes.append(img_list)
        
        return classes

    # n batch should have p random, but distinct images from each class
    # Each batch should have no duplicates
    def load_batches(self, n, p):
        classes = self.load_classes()
        batches = []
        for i in range(n):
            batch = []
            for c in classes:
                selection = random.sample(c, p)
                batch.extend(selection)
                [img_tag_pair for img_tag_pair in c if img_tag_pair not in selection]
            batches.append(batch)
        return batches