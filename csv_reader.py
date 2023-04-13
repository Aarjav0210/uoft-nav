import os
import pandas as pd
from street_viewer import StreetViewer


#read csv file
class CSVReader(object):
    def __init__(self, filename):
        self.filename = filename
        self.filepath = os.path.join(os.getcwd(), filename)
        self.df = pd.read_csv(self.filepath)

    #return list of all tags from the 'tag' column
    def get_all_tags(self):
        #dont add any tags that have a 'N/A' in for LatLong
        df = self.df
        df = df[df['LatLong'] != 'N/A']
        tags = df['Tag'].tolist()
        return tags

    def get_row(self, tag):
        #get row from csv file
        df = self.df
        row = df.loc[df['Tag'] == tag]
        #return row as a dict
        return row.to_dict('records')[0]

    def print_row(row):
        print(row)

    def get_image(self, tag, api_key):
        row = self.get_row(tag)
        location = row['LatLong']
        fov = row['FOV']
        heading = row['Heading']
        pitch = row['Pitch']
        image_viewer = StreetViewer(api_key=api_key, location=location, fov=fov, heading=heading, pitch=pitch, verbose=True, tag=tag)
        image_viewer.get_meta()
        image_viewer.get_pic()
        # image_viewer.display_pic()