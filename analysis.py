import os
import re
import glob
from argparse import ArgumentParser
import pandas as pd

from yolo_object_detector import ObjectDetector
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

pd.options.mode.chained_assignment = None  # default='warn'

parser = ArgumentParser()
parser.add_argument('-n', '--name', dest='csv_name', help='csv file name', metavar='FOLDER')
parser.add_argument('-c', '--csv', dest='csv_folder_name', help='csv folder name', metavar='CSV_FOLDER', default='csv_data_hate')
args = parser.parse_args()

csv_name = args.csv_name
csv_folder_name = args.csv_folder_name

# -------------------------------------
# Get objects in the images as a string
# -------------------------------------
print('Get object classes in the image')

csv_path = csv_folder_name + '/' + csv_name + '.csv'
df_csv = pd.read_csv(csv_path, index_col=False)

detector = ObjectDetector()
df_csv['image_objects'] = df_csv['image_path'].apply(detector.detect_objects_in_image)
# df_csv_cleaned = df_csv[df_csv.has_object.eq(1)]
# df_csv_cleaned.drop(columns=['YOLO_object'], inplace=True)
# df_csv_cleaned.reset_index(drop=True, inplace=True)

result_path = csv_folder_name + '/' + csv_name + '_anal_obj.csv'
df_csv.to_csv(result_path, index=False)

# count the tweets in different hashtags after cleaning
# print(df_csv_cleaned['hashtag'].value_counts())
# print('Topic: {} - Images with objects: {:>5}'.format(folder_name, len(df_csv_cleaned.index)))
print()

# -------------------------------------
# Sentimental Analysis on OCR text
# -------------------------------------
print('Vader Sentimental Analysis Start')

csv_path = csv_folder_name + '/' + csv_name + '_anal_obj.csv'
# csv_path = 'csv_data_hate/sample_google_no_politics.csv'
df_csv = pd.read_csv(csv_path, index_col=False)
# sentences = list(df_csv['image_text'])
analyzer = SentimentIntensityAnalyzer()


# print(df_csv.info())
df_csv.image_text = df_csv.image_text.fillna('')
df_csv['image_text_NLP'] = df_csv['image_text'].apply(analyzer.polarity_scores)

# df_csv_cleaned = df_csv[df_csv.has_object.eq(1)]
# df_csv_cleaned.drop(columns=['YOLO_object'], inplace=True)
# df_csv_cleaned.reset_index(drop=True, inplace=True)

result_path = csv_folder_name + '/' + csv_name + '_anal_obj_text.csv'
df_csv.to_csv(result_path, index=False)

# count the tweets in different hashtags after cleaning
# print(df_csv_cleaned['hashtag'].value_counts())
# print('Topic: {} - Images with objects: {:>5}'.format(folder_name, len(df_csv_cleaned.index)))
print()