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
        tags = self.df['Tag'].tolist()
        return tags

    def get_row(self, tag):
        df = self.df
        row = df.loc[df['Tag'] == tag]
        return row.to_dict('records')[0]

    def print_row(row):
        print(row)