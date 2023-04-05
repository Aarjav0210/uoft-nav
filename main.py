
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import os
from dotenv import load_dotenv

load_dotenv()

meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
pic_base = 'https://maps.googleapis.com/maps/api/streetview?'

location = '88 King\'s College Cir, Toronto, ON M5S'

# define the params for the metadata request
meta_params = {'key': os.getenv('API_KEY'),
               'location': location
               }
# define the params for the picture request
pic_params = {'key': os.getenv('API_KEY'),
              'location': location,
              'size': '640x640'
              }

# obtain the metadata of the request (this is free)
meta_response = requests.get(meta_base, params=meta_params)
print(meta_response.json())

pic_response = requests.get(pic_base, params=pic_params)

for key, value in pic_response.headers.items():
    print(f"{key}: {value}")

print(pic_response.ok)

filename = './images/test.jpg' 

with open(filename, 'wb') as file:
    file.write(pic_response.content)
# remember to close the response connection to the API
pic_response.close()

plt.figure(figsize=(10, 10))
img=mpimg.imread(filename)
imgplot = plt.imshow(img)
plt.show()