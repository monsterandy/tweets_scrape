import os
import glob
from argparse import ArgumentParser
import pandas as pd
from tqdm import tqdm

pd.options.mode.chained_assignment = None  # default='warn'

parser = ArgumentParser()
parser.add_argument('-n', '--name', dest='folder_name', help='folder name', metavar='FOLDER')
args = parser.parse_args()

folder_name = args.folder_name
folder_path = 'tweet_data/' + folder_name + '/'

def get_image_path(image_url, csv_path):
    image_name = image_url.split('/')[-1]
    image_path = './' + csv_path[:-4] + '/' + image_name
    return image_path

