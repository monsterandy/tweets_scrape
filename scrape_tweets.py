#!/usr/bin/env python
# coding: utf-8

from config import consumer_key, consumer_secret, access_token, access_token_secret

import os
import glob
from pathlib import Path
import pandas as pd
import tweepy


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


entries = os.listdir('data/')

text = []
for i in entries:
    listfiles = glob.glob('data/'+i+'/*.txt')
    for entry in listfiles:
        entry_path = Path(entry[:-3] + 'csv')
        if not entry_path.exists():
            text.append(entry)


# Fetching all the tweet data
def fetch_tw(ids, csv_path):
    tw_statuses = api.statuses_lookup(ids, tweet_mode="extended")

    data = pd.DataFrame(columns=['media', 'text_data', 'tweet_id', 'tweet_url'])
    for status in tw_statuses:
        if('media' in status.entities) and status.lang == 'en':
            # print('{} - lang: {}'.format(status.id, status.lang))
            tweet_elem = {"tweet_id": status.id,
                          "media": status.entities['media'][0]['media_url'], "text_data": status.full_text, 'tweet_url': 'https://twitter.com/i/web/status/'+status.id_str}
            data = data.append(tweet_elem, ignore_index=True)

    # if file does not exist, write header
    if not os.path.isfile(csv_path[:-4]+'.csv'):
        data.to_csv(csv_path[:-4]+".csv", index=False)
    else:  # else it exists so append without writing the header
        data.to_csv(csv_path[:-4]+".csv", mode='a', header=False, index=False)


for path in text:
    tweet_url = pd.read_csv(path, index_col=None,
                            header=None, names=["tweet_urls"])

    def af(x): return x["tweet_urls"].split("/")[-1]
    # store tweet id in another column
    tweet_url['tweet_id'] = tweet_url.apply(af, axis=1)
    ids = tweet_url['tweet_id'].tolist()
    total_count = len(ids)
    if total_count == 0:
        data = pd.DataFrame(
            columns=['media', 'text_data', 'tweet_id', 'tweet_url'])
        data.to_csv(path[:-4]+".csv", index=False)

    print('{} tweets in file {}'.format(total_count, path))

    chunks = (total_count - 1) // 50 + 1
    for i in range(chunks):
        lst = ids[i*50:(i+1)*50]
        fetch_tw(lst, path)
