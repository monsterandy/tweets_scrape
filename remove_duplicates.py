# import the necessary packages
from imutils import paths
import numpy as np
import argparse
import cv2
import os
import pandas as pd


def dhash(image, hashSize=8):
    # convert the image to grayscale and resize the grayscale image,
    # adding a single column (width) so we can compute the horizontal
    # gradient
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (hashSize + 1, hashSize))
    # compute the (relative) horizontal gradient between adjacent
    # column pixels
    diff = resized[:, 1:] > resized[:, :-1]
    # convert the difference image to a hash and return it
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


# grab the paths to all images in our input dataset directory and
# then initialize our hashes dictionary
# imagePaths = list(paths.list_images(args["dataset"]))
# cleaned_data = pd.read_csv('../tweets_scrape/csv_data/data_AsianHate_cleaned.csv',index_col=0)
# imagePaths = cleaned_data['image_path'].to_list()
hashes = {}


def duplicate_detector(imagePaths):
    # loop over our image paths
    for imagePath in imagePaths:
        # print("{}/{} is being processed, {}".format(imagePaths.index(imagePath) +
        #       1, len(imagePaths), imagePath))
        # load the input image and compute the hash
        image = cv2.imread(imagePath)
        try:
            image = cv2.resize(image, (150, 150))
        except cv2.error:
            continue
        h = dhash(image)
        # grab all image paths with that hash, add the current image
        # path to it, and store the list back in the hashes dictionary
        p = hashes.get(h, [])
        p.append(imagePath)
        hashes[h] = p
    no_duplicate_paths = []
    for i, hashedPaths in hashes.items():
        no_duplicate_paths.append(hashedPaths[0])
    return no_duplicate_paths
