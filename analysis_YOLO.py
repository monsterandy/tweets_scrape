import os
import re
import glob
from argparse import ArgumentParser
import pandas as pd
# import spacy

from opencv_text_detector import TextDetector
from remove_duplicates import duplicate_detector
from yolo_object_detector import ObjectDetector
from tesseract_ocr import threshold_ocr

pd.options.mode.chained_assignment = None  # default='warn'

parser = ArgumentParser()
parser.add_argument('-n', '--name', dest='folder_name', help='data folder name', metavar='FOLDER')
parser.add_argument('-c', '--csv', dest='csv_folder_name', help='csv folder name', metavar='CSV_FOLDER', default='csv_data_hate')
args = parser.parse_args()

folder_name = args.folder_name
csv_folder_name = args.csv_folder_name
entry_folder = 'tweet_data/' + folder_name + '/'

# def get_image_path(image_url, csv_path):
#     image_name = image_url.split('/')[-1]
#     image_path = './' + csv_path[:-4] + '/' + image_name
#     return image_path

# df_csv = pd.DataFrame(columns=['hashtag', 'tweet_id', 'image_path', 'body_text'])
# df_csv['tweet_id'] = df_csv['tweet_id'].astype('int64')

# entries = os.listdir(entry_folder)
# for hashtag in entries:
#     if hashtag.startswith('.'): continue
#     list_files = glob.glob(entry_folder + hashtag + '/*.csv')
#     tweets_count = 0
#     for csv_path in list_files:
#         # print(csv_path)
#         temp_df = pd.read_csv(csv_path)
#         tweets_count += len(temp_df.index)
#         temp_df.drop(columns=['tweet_url'], inplace=True)
#         temp_df.rename({'text_data': 'body_text', 'media': 'image_path'}, axis='columns', inplace=True)
#         temp_df.insert(loc=0, column='hashtag', value=hashtag)
#         cols = temp_df.columns.tolist()
#         # before: cols = ['hashtag', 'image_path', 'body_text', 'tweet_id']
#         cols = cols[:1] + cols[-1:] + cols[1:-1]
#         temp_df = temp_df[cols]
#         temp_df['image_path'] = temp_df['image_path'].apply(get_image_path, csv_path=csv_path)
#         temp_df['tweet_id'] = temp_df['tweet_id'].astype('int64')
#         df_csv = df_csv.append(temp_df)
#     print('{:>30s}: {:>5}'.format(hashtag, tweets_count))
# print('Topic: {} - Total images: {:>5}'.format(folder_name, len(df_csv.index)))

# remove tweets with invalid image path
# df_csv['path_is_valid'] = df_csv['image_path'].apply(lambda x: 1 if os.path.isfile(x) else 0)
# df_csv = df_csv[df_csv.path_is_valid.eq(1)]
# df_csv.drop(columns=['path_is_valid'], inplace=True)

# df_csv.reset_index(drop=True, inplace=True)

# result_path = csv_folder_name + '/' + folder_name + '.csv'
# df_csv.to_csv(result_path)
# print()

# -------------------------------------
# Filter out images with no objects
# -------------------------------------
print('Get object classes in the image')

csv_path = csv_folder_name + '/' + folder_name + '_final.csv'
df_csv = pd.read_csv(csv_path, index_col=0)
detector = ObjectDetector()

df_csv['YOLO_object'] = df_csv['image_path'].apply(detector.detect_objects_in_image)
# df_csv_cleaned = df_csv[df_csv.has_object.eq(1)]
# df_csv_cleaned.drop(columns=['YOLO_object'], inplace=True)
# df_csv_cleaned.reset_index(drop=True, inplace=True)

result_path = csv_folder_name + '/' + folder_name + '_anal_YOLO.csv'
df_csv.to_csv(result_path)

# count the tweets in different hashtags after cleaning
# print(df_csv_cleaned['hashtag'].value_counts())
# print('Topic: {} - Images with objects: {:>5}'.format(folder_name, len(df_csv_cleaned.index)))
print()