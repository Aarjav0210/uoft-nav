# requests and json are the dependencies
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from dotenv import load_dotenv


class StreetViewer(object):
    def __init__(self, api_key, location, tag, size="224x224", fov=90, heading=9999, pitch=0,
                 folder_directory='./images/', verbose=True):
        """
        This class handles a single API request to the Google Static Street View API
        api_key: obtain it from your Google Cloud Platform console
        location: the address string or a (lat, lng) tuple
        size: returned picture size. maximum is 640*640
        folder_directory: directory to save the returned objects from request
        verbose: whether to print the processing status of the request
        """
        # input params are saved as attributes for later reference
        self._key = api_key
        self.location = location
        self.size = size
        self.folder_directory = folder_directory
        self.fov = fov
        self.pitch = pitch
        self.heading = heading
        # call params are saved as internal params
        self._meta_params = dict(key=self._key,
                                location=self.location)
        self._pic_params = dict(key=self._key,
                               location=self.location,
                               size=self.size,
                               fov=self.fov,
                               heading=self.heading)
        self.verbose = verbose
        self.tag = tag
    
    def get_meta(self):
        """
        Method to query the metadata of the address
        """
        self._meta_response = requests.get(
            'https://maps.googleapis.com/maps/api/streetview/metadata?',
            params=self._meta_params)
        self.meta_info = self._meta_response.json()
        self.meta_status = self.meta_info['status']
        if self._meta_response.ok:
            if self.verbose:
                print(">>> Obtained Meta from StreetView API:")
                print(self.meta_info)
        else:
            print(">>> Failed to obtain Meta from StreetView API!!!")
        self._meta_response.close()
        return self.meta_info

    def get_pic(self):
        """
        Method to query the StreetView picture and return image content as bytes
        """
        if self.meta_status == 'OK':
            if self.verbose:
                print(">>> Picture available, requesting now...")
            self._pic_response = requests.get(
                'https://maps.googleapis.com/maps/api/streetview?',
                params=self._pic_params)
            self.pic_header = dict(self._pic_response.headers)
            if self._pic_response.ok:
                if self.verbose:
                    print(">>> COMPLETE!")
                return self._pic_response.content
        else:
            print(">>> Picture not available in StreetView, ABORTING!")

    def display_pic(self):
        """
        Method to display the downloaded street view picture if available
        """
        if self.meta_status == 'OK':
            plt.figure(figsize=(10, 10))
            img=mpimg.imread(self.pic_path)
            imgplot = plt.imshow(img)
            plt.show()
        else:
            print(">>> Picture not available in StreetView, ABORTING!")