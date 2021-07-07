#!/usr/bin/env python
# coding: utf-8

import glob
import os
from pathlib import Path
import requests
import pandas as pd
from tqdm import tqdm

entries = os.listdir('data/')
text = []
for i in entries:
    listfiles = glob.glob('data/'+i+'/*.csv')
    for entry in listfiles:
        entry_path = Path(entry[:-4])
        if not entry_path.exists():
            text.append(entry)
            os.system('mkdir ' + entry[:-4])


print('CSV FILE COUNT: {}'.format(len(text)))
for path in tqdm(text):
    data = pd.read_csv(path, index_col=False)
    for i in tqdm(data['media'], leave=False):
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
