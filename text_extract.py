import os
from argparse import ArgumentParser
import pandas as pd
from google_cloud_api import GoogleVision

pd.options.mode.chained_assignment = None  # default='warn'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/user/zheyuanm/credentials/cloud_vision_credential.json'

parser = ArgumentParser()
parser.add_argument('-c', '--csv', dest='csv_path', help='csv file path', metavar='CSV_PATH')
args = parser.parse_args()

csv_path = args.csv_path

df_csv = pd.read_csv(csv_path, index_col=False)
# df_csv_test = df_csv[:100]

print(len(df_csv.index))

client = GoogleVision()
df_csv['labels'], df_csv['safe_search'] = zip(*df_csv['image_path'].apply(client.detect_label_safesearch))

df_csv.to_csv(csv_path, index=False)
# df_csv_test.to_csv('csv_data_hate/hate_cleaned_test.csv', index=False)
