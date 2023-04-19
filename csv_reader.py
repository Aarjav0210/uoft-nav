import os
import pandas as pd
from street_viewer import StreetViewer


#read csv file
class CSVReader(object):
    def __init__(self, filename):
        self.filename = filename
        self.filepath = os.path.join(os.getcwd(), filename)
        df = pd.read_csv(self.filepath)
        self.df = df.dropna(subset=['LatLong'])


    #return list of all tags from the 'tag' column
    def get_all_tags(self):
        #dont add any tags that have a 'N/A' in for LatLong
        # df = self.df
        # #remove files that have 'N/A' for LatLong
        # df = df[df['LatLong'] != 'nan']
        tags = self.df['Tag'].tolist()
        return tags

    def get_row(self, tag):
        #get row from csv file
        df = self.df
        row = df.loc[df['Tag'] == tag]
        #return row as a dict
        return row.to_dict('records')[0]

    def print_row(row):
        print(row)

    # def get_image(self, tag, api_key, location=None, fov=None, heading=None, pitch=None):
    #     row = self.get_row(tag)
    #     if location == None:
    #         location = row['LatLong']
    #     if fov == None:
    #         fov = row['FOV']
    #     if heading == None:
    #         heading = row['Heading']
    #     if pitch == None:
    #         pitch = row['Pitch']
            
    #     image_viewer = StreetViewer(api_key=api_key, location=location, fov=fov, heading=heading, pitch=pitch, verbose=True, tag=tag)
    #     image_viewer.get_meta()
    #     image_viewer.get_pic()
        # image_viewer.display_pic()

# csv = CSVReader('uoft_locations.csv')
# print(len(csv.get_all_tags()))
# # get all rows and print all latlongs
# for tag in csv.get_all_tags():
#     print(csv.get_row(tag)['LatLong'])