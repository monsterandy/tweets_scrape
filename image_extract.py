#!/usr/bin/env python
# coding: utf-8

import glob
import os
from pathlib import Path
from argparse import ArgumentParser
import requests
import pandas as pd
from tqdm import tqdm

parser = ArgumentParser()
parser.add_argument('-n', '--name', dest='folder_name', help='folder name', metavar='FOLDER')
args = parser.parse_args()

folder_name = args.folder_name
folder_path = 'tweet_data_general/' + folder_name + '/'

entries = os.listdir(folder_path)
text = []
for i in entries:
    listfiles = glob.glob(folder_path + i + '/*.csv')
    for entry in listfiles:
        entry_path = Path(entry[:-4])
        if not entry_path.exists():
            text.append(entry)
            os.system('mkdir ' + entry[:-4])


print('CSV FILE COUNT: {}'.format(len(text)))
for path in tqdm(text, miniters=1):
    data = pd.read_csv(path, index_col=False)
    for i in data['media']:
        image_url = i
    #     print(image_url)
        if pd.isnull(image_url):
            continue
    #     print(image_url)
        elif '.jpg' or '.png' in image_url:
            try:
                r = requests.get(image_url)  # create HTTP response object
                img_name = image_url.split('/')[-1]
                # send a HTTP request to the server and save
                # the HTTP response in a response object called r
                with open(path[:-4]+'/'+img_name, 'wb') as f:

                    # Saving received content as a png file in
                    # binary format

                    # write the contents of the response (r.content)
                    # to a new file in binary mode.
                    f.write(r.content)
                    # print("SUCCESS {}".format(path[:-4]+'/'+img_name))
            except:
                print("FAILED AT PATH: {}, URL: {}".format(path, image_url))
