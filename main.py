
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from street_viewer import StreetViewer
import pandas as pd
import os
from dotenv import load_dotenv
from csv_reader import CSVReader
from noise_generator import NoiseGenerator
from data_loader import DataLoader

import numpy as np

import splitfolders

#load API key
load_dotenv()

#load data from csv file
filename = 'uoft_locations.csv'
dl = DataLoader(filename, api_key=os.getenv('API_KEY'))
dl.save_all_images()
