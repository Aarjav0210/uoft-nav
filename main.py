api_key = "AIzaSyAjNTixnCRC4OMFDSC2rO166XBRBPl_n_c"

import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
pic_base = 'https://maps.googleapis.com/maps/api/streetview?'

location = '27 King\'s College Cir, Toronto, ON M5S'

meta_params = {'key': api_key, 'location': location}
pic_params = {'key': api_key, 'location': location, 'size': '640x640'}

meta_response = requests.get(meta_base, params=meta_params)
#print(meta_response.json())

pic_response = requests.get(pic_base, params=pic_params)

for key, value in pic_response.headers.items():
    print(f"{key}: {value}")

with open('test.jpg', 'wb') as file:
    file.write(pic_response.content)
# remember to close the response connection to the API
pic_response.close()

plt.figure(figsize=(10, 10))
img=mpimg.imread('test.jpg')
imgplot = plt.imshow(img)
plt.show()
