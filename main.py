
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#Get access to functions from streetview.py
from streetview import StreetViewer
#for csv file
import pandas as pd
import os
from dotenv import load_dotenv
from csv_reader import CSVReader

#load API key
load_dotenv()

#load data from csv file
filename = 'uoft_locations.csv'
uoft_data = CSVReader(filename)

#Get image
uoft_data.get_image(uoft_data.get_all_tags()[0])

