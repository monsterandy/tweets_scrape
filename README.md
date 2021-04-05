# tweets_scrape

## An automatic tool to scrape tweets with images

### Prerequisites

- [snscrape](https://github.com/JustAnotherArchivist/snscrape) is a scraper for social networking services (SNS).
- [tweepy](https://github.com/itsayushisaxena/tweepy) is a library of Python to access Twitter API (If you use Python 3.9 or higher, please install the developer version).
- A twitter developer account alongwith the API credentials. 
- Rename the `config_example.py` file to `config.py`. In this file, you need to modify the hashtags and time period to what you want. Also, add your Twitter API credentials in this file.


### Scripts

`autocommand.py` - This file is to get tweet URLs in a particular time period. It can generate the [`snscrape`](https://github.com/JustAnotherArchivist/snscrape) commands in seven-day period.

`scrape_tweets.py` - This file is to get the tweet data like media_url, text_data in the tweet, etc., from URLs we got from above and save them into a .csv file. This part needs Twitter API keys, so please put your own API keys in the `config.py` file.

`image_extract.py` - This file is to get the images from the media_url of each tweet.

