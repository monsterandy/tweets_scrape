import os
import re
import glob
from argparse import ArgumentParser
import pandas as pd
import spacy

from opencv_text_detector import TextDetector
from remove_duplicates import duplicate_detector
from yolo_object_detector import ObjectDetector
from tesseract_ocr import threshold_ocr

pd.options.mode.chained_assignment = None  # default='warn'

parser = ArgumentParser()
parser.add_argument('-n', '--name', dest='folder_name', help='data folder name', metavar='FOLDER')
parser.add_argument('-c', '--csv', dest='csv_folder_name', help='csv folder name', metavar='CSV_FOLDER', default='csv_data_general')
args = parser.parse_args()

folder_name = args.folder_name
csv_folder_name = args.csv_folder_name
entry_folder = 'tweet_data_general/' + folder_name + '/'

def get_image_path(image_url, csv_path):
    image_name = image_url.split('/')[-1]
    image_path = './' + csv_path[:-4] + '/' + image_name
    return image_path

df_csv = pd.DataFrame(columns=['hashtag', 'tweet_id', 'image_path', 'body_text'])
df_csv['tweet_id'] = df_csv['tweet_id'].astype('int64')

entries = os.listdir(entry_folder)
for hashtag in entries:
    if hashtag.startswith('.'): continue
    list_files = glob.glob(entry_folder + hashtag + '/*.csv')
    tweets_count = 0
    for csv_path in list_files:
        # print(csv_path)
        temp_df = pd.read_csv(csv_path)
        tweets_count += len(temp_df.index)
        temp_df.drop(columns=['tweet_url'], inplace=True)
        temp_df.rename({'text_data': 'body_text', 'media': 'image_path'}, axis='columns', inplace=True)
        temp_df.insert(loc=0, column='hashtag', value=hashtag)
        cols = temp_df.columns.tolist()
        # before: cols = ['hashtag', 'image_path', 'body_text', 'tweet_id']
        cols = cols[:1] + cols[-1:] + cols[1:-1]
        temp_df = temp_df[cols]
        temp_df['image_path'] = temp_df['image_path'].apply(get_image_path, csv_path=csv_path)
        temp_df['tweet_id'] = temp_df['tweet_id'].astype('int64')
        df_csv = df_csv.append(temp_df)
    print('{:>30s}: {:>5}'.format(hashtag, tweets_count))
print('Topic: {} - Total images: {:>5}'.format(folder_name, len(df_csv.index)))

# remove tweets with invalid image path
df_csv['path_is_valid'] = df_csv['image_path'].apply(lambda x: 1 if os.path.isfile(x) else 0)
df_csv = df_csv[df_csv.path_is_valid.eq(1)]
df_csv.drop(columns=['path_is_valid'], inplace=True)

df_csv.reset_index(drop=True, inplace=True)

result_path = csv_folder_name + '/' + folder_name + '.csv'
df_csv.to_csv(result_path)
print()

# -------------------------------------
# Filter out images without text
# -------------------------------------
print('Filter out images without text')

detector = TextDetector()
df_csv['has_text'] = df_csv['image_path'].apply(detector.detect_text)

# filter out those images without text
df_csv_cleaned = df_csv[df_csv.has_text.eq(1)]
df_csv_cleaned.drop(columns=['has_text'], inplace=True)
df_csv_cleaned.reset_index(drop=True, inplace=True)

result_path = csv_folder_name + '/' + folder_name + '_wt.csv'
df_csv_cleaned.to_csv(result_path)

# count the tweets in different hashtags after cleaning
print(df_csv_cleaned['hashtag'].value_counts())
print('Topic: {} - Images with text: {:>5}'.format(folder_name, len(df_csv_cleaned.index)))
print()

# -------------------------------------
# Filter out duplicate images
# -------------------------------------
print('Filter out duplicate images')

csv_path = csv_folder_name + '/' + folder_name + '_wt.csv'
df_csv = pd.read_csv(csv_path, index_col=0)
image_paths = df_csv['image_path'].to_list()
no_dup_paths = duplicate_detector(image_paths)

df_csv['no_dups'] = df_csv['image_path'].apply(lambda x: 1 if x in no_dup_paths else 0)
df_csv_cleaned = df_csv[df_csv.no_dups.eq(1)]
df_csv_cleaned.drop(columns=['no_dups'], inplace=True)
df_csv_cleaned.reset_index(drop=True, inplace=True)

result_path = csv_folder_name + '/' + folder_name + '_wt_nd.csv'
df_csv_cleaned.to_csv(result_path)

# count the tweets in different hashtags after cleaning
print(df_csv_cleaned['hashtag'].value_counts())
print('Topic: {} - Images without duplication: {:>5}'.format(folder_name, len(df_csv_cleaned.index)))
print()

# -------------------------------------
# Filter out images with no objects
# -------------------------------------
print('Filter out images with no objects')

csv_path = csv_folder_name + '/' + folder_name + '_wt_nd.csv'
df_csv = pd.read_csv(csv_path, index_col=0)
detector = ObjectDetector()

df_csv['has_object'] = df_csv['image_path'].apply(detector.detect_object)
df_csv_cleaned = df_csv[df_csv.has_object.eq(1)]
df_csv_cleaned.drop(columns=['has_object'], inplace=True)
df_csv_cleaned.reset_index(drop=True, inplace=True)

result_path = csv_folder_name + '/' + folder_name + '_wt_nd_wo.csv'
df_csv_cleaned.to_csv(result_path)

# count the tweets in different hashtags after cleaning
print(df_csv_cleaned['hashtag'].value_counts())
print('Topic: {} - Images with objects: {:>5}'.format(folder_name, len(df_csv_cleaned.index)))
print()

# -------------------------------------
# Extract text from images using Tesseract
# -------------------------------------
print('Extract text from images using Tesseract')

csv_path = csv_folder_name + '/' + folder_name + '_wt_nd_wo.csv'
df_csv = pd.read_csv(csv_path, index_col=0)

df_csv['text_with_OCR'] = df_csv['image_path'].apply(threshold_ocr)

result_path = csv_folder_name + '/' + folder_name + '_wt_nd_wo_locr.csv'
df_csv.to_csv(result_path)
print()

# -------------------------------------
# Clean the OCR results
# -------------------------------------
print('Clean the OCR results')

csv_path = csv_folder_name + '/' + folder_name + '_wt_nd_wo_locr.csv'
df_csv = pd.read_csv(csv_path, index_col=0)

nlp = spacy.load('en_core_web_md',disable = ['parser','ner']) # remove three tasks so as to speed up the precess 
nlp.max_length = 1100000

def nlp_preprocess(caption):
    doc = nlp(caption)
    lemmanized_list = []
    lemmanized_phrase = ""
    for token in doc:
        if not token.is_punct and not token.is_stop and not token.is_oov: # check is token is not punctutation stop word and in the nlp vocab
            lemmanized_list.append(token.lemma_.lower().strip() if token.lemma_ != "-PRON-" else token.text) 
    lemmanized_phrase = ' '.join(lemmanized_list)
    return lemmanized_phrase

# remove line breakers
df_csv['text_with_OCR'] = df_csv['text_with_OCR'].apply(lambda x: x.replace('\n', ' '))
# tokenize, remove words that are shorted than two characters ,lemmatizer, removing stopwords, and stemming
df_csv['text_with_OCR'] = df_csv['text_with_OCR'].apply(nlp_preprocess)
# remove any single character
df_csv['text_with_OCR'] = df_csv['text_with_OCR'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>1]))

df_csv['word_count'] = df_csv['text_with_OCR'].apply(lambda x: len(re.findall(r'\w+', x)))
df_csv = df_csv[df_csv.word_count.lt(21)]

def is_nonsense_detection(text):
    total_words = len(re.findall(r'\w+', text))
    # total words equal to 0 - discard it
    if total_words == 0: return 1
    # if a detectiion contains long word(s), consider it as a valid detection
    long_words = len([word for word in text.split() if len(word)>=5])
    if long_words > 0: return 0
    # if a text without any long word has 5 or less words, discard it
    if total_words <= 5: return 1
    # if nonsense words dominates the detection, discard it
    invalid_words = len([word for word in text.split() if len(word)<=3])
    invalid_prop = invalid_words / total_words
    if invalid_prop > 0.75 and total_words > 0: return 1
    else: return 0

df_csv['is_invalid'] = df_csv['text_with_OCR'].apply(is_nonsense_detection)
df_csv_cleaned = df_csv[df_csv.is_invalid.eq(0)]
df_csv_cleaned.drop(columns=['word_count', 'is_invalid'], inplace=True)
df_csv_cleaned.reset_index(drop=True, inplace=True)

result_path = csv_folder_name + '/' + folder_name + '_final.csv'
df_csv_cleaned.to_csv(result_path)

# count the tweets in different hashtags after cleaning
print(df_csv_cleaned['hashtag'].value_counts())
print('Topic: {} - Images after Tesseract: {:>5}'.format(folder_name, len(df_csv_cleaned.index)))
print()