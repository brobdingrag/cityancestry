from inventory import *

# Latitude and longitude of Times Square, the center of the rectangular map
LAT_TIMSQ, LON_TIMSQ = 40.758896, -73.985130

# Define map dimensions
LAT_HEIGHT = 0.5  # Latitude range
LON_WIDTH = 0.7   # Longitude range

N_PEOPLE_PER_DOT = 30  # was 25  

DOT_SIZE = 220  # was 200

DPI = 800  # was 1000

IMAGE_WIDTH = 14  # inches - was 14 with 0.7 x 0.5  -  w x h

TILES = 'CartoDB.DarkMatter'  # Dark mode background

RACES = ['W', 'H', 'B', 'A']
RACE_COLORS = {'W': '#1f77b4', 'H': '#ff7f0e', 'B': '#d62728', 'A': '#2ca02c'}

BLACK_UNDERCOUNT_2020 = 0.05
BLACK_UNDERCOUNT_2010 = 0.02
HISP_UNDERCOUNT_2020 = 0.06
HISP_UNDERCOUNT_2010 = 0.03
WHITE_OVERCOUNT_2020 = 0.02
WHITE_OVERCOUNT_2010 = 0.01

PERCENT_OTHER_ASIAN = 0.6  # Relevant for 1970 and earlier


class Corners:
    """
    Defines the corners of the map. Hardcoded into index.html.
    """
    def __init__(self):
        self.center_lon = LON_TIMSQ
        self.center_lat = LAT_TIMSQ
        
        # Calculate boundaries based on center coordinates
        self.min_lon = self.center_lon - LON_WIDTH / 2
        self.max_lon = self.center_lon + LON_WIDTH / 2
        self.min_lat = self.center_lat - LAT_HEIGHT / 2
        self.max_lat = self.center_lat + LAT_HEIGHT / 2

    def copy(self):
        copy(self.__dict__)

        