# for general hashtags

import os
from pathlib import Path
from argparse import ArgumentParser
from datetime import timedelta, datetime

parser = ArgumentParser()
parser.add_argument('-t', '--topic', dest='topic_name', help='topic name', metavar='TOPIC')
parser.add_argument('-s', '--start', dest='start_date', help='start date in YYYY-mm-dd', metavar='START')
parser.add_argument('-e', '--end', dest='end_date', help='end date in YYYY-mm-dd', metavar='END')
args = parser.parse_args()

topic_name = args.topic_name
start_date = datetime.strptime(args.start_date, '%Y-%m-%d').date()
end_date = datetime.strptime(args.end_date, '%Y-%m-%d').date()
if start_date.year == 2021:
    month = '2021-{:02d}'.format(start_date.month)
else:
    month = '2020-{:02d}'.format(start_date.month)

hashtag_path = 'hashtag_list/general/' + topic_name
with open(hashtag_path) as file:
    hashtags = [line.rstrip('\n') for line in file]

if not Path('tweet_data_general/').exists():
    os.system('mkdir tweet_data_general')

data_path = 'tweet_data_general/' + topic_name + '_' + month + '/'
if not Path(data_path).exists():
    os.system('mkdir ' + data_path)

# making directories for each hashtags
for i in range(len(hashtags)):
    if not Path(data_path + hashtags[i]).exists():
        os.system('mkdir ' + data_path + hashtags[i])

command_list = []
for i in range(len(hashtags)):
    delta = timedelta(days=(7-1))
    cycle = 1
    start_date_cycle = start_date

    while start_date_cycle <= end_date:
        # make sure the next cycle not exceed the until date
        if start_date_cycle + delta < end_date:
            end_date_cycle = start_date_cycle + delta
        else:
            end_date_cycle = end_date
        
        cycle_command = 'snscrape twitter-search' + ' "#' + \
            hashtags[i]+' since:' + str(start_date_cycle) + ' until:' + str(end_date_cycle) + \
            ' filter:images" > '+ data_path + hashtags[i]+'/tweets' + str(cycle) + '.txt'
        command_list.append(cycle_command)

        # add 7 days to circle
        start_date_cycle += delta + timedelta(days=1)
        cycle += 1

# with open('commands.txt', 'w') as f:
#     for item in command_list:
#         f.write("%s\n" % item)

# file1 = open('commands.txt', 'r')
# command_list = file1.readlines()
# print(command_list)
for i in command_list:
    print(i)
    os.system(i)
