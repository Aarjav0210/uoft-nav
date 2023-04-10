
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#Get access to functions from streetview.py
from streetview import StreetViewer
#for csv file
import pandas as pd
#for API key
import os
from dotenv import load_dotenv

#load API key
load_dotenv()


#read csv file
def read_csv(filename):
    path_to_file = os.path.join(os.getcwd(), filename)
    df = pd.read_csv(path_to_file)
    return df

#return list of all tags from the 'tag' column
def get_all_tags(df):
    #dont add any tags that have a 'N/A' in for LatLong
    df = df[df['LatLong'] != 'N/A']
    tags = df['Tag'].tolist()
    return tags

def get_row(df, tag):
    #get row from csv file
    row = df.loc[df['Tag'] == tag]
    #return row as a dict
    return row.to_dict('records')[0]

def print_row(row):
    print(row)

uoft_locations_df = read_csv('uoft_locations.csv')
# print_row(get_row(uoft_locations_df, get_all_tags(uoft_locations_df)[0]))
# print_row(get_row(uoft_locations_df, get_all_tags(uoft_locations_df)[1]))


def get_image(tag):
    row = get_row(uoft_locations_df, tag)
    location = row['LatLong']
    fov = row['FOV']
    heading = row['Heading']
    pitch = row['Pitch']
    image_viewer = StreetViewer(api_key=os.getenv('API_KEY'), location=location, fov=fov, heading=heading, pitch=pitch, verbose=True)
    image_viewer.get_meta()
    image_viewer.get_pic()
    image_viewer.display_pic()

get_image(get_all_tags(uoft_locations_df)[0])

# image_viewer = StreetViewer(api_key=os.getenv('API_KEY'), location='88 King\'s College Cir, Toronto, ON M5S', verbose=True)

# meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
# pic_base = 'https://maps.googleapis.com/maps/api/streetview?'

# location = '88 King\'s College Cir, Toronto, ON M5S'

# # define the params for the metadata request
# meta_params = {'key': os.getenv('API_KEY'),
#                'location': location
#                }
# # define the params for the picture request
# pic_params = {'key': os.getenv('API_KEY'),
#               'location': location,
#               'size': '640x640'
#               }

# # obtain the metadata of the request (this is free)
# meta_response = requests.get(meta_base, params=meta_params)
# print(meta_response.json())

# pic_response = requests.get(pic_base, params=pic_params)

# for key, value in pic_response.headers.items():
#     print(f"{key}: {value}")

# print(pic_response.ok)

# filename = './images/test.jpg' 

# with open(filename, 'wb') as file:
#     file.write(pic_response.content)
# # remember to close the response connection to the API
# pic_response.close()

# plt.figure(figsize=(10, 10))
# img=mpimg.imread(filename)
# imgplot = plt.imshow(img)
# plt.show()
