from config import hashtags, start_date, until_date

import os
from pathlib import Path

from datetime import date, timedelta

if not Path('data/').exists():
    os.system('mkdir data')

# making directories for each hashtags
for i in range(len(hashtags)):
    if not Path('data/' + hashtags[i][1:]).exists():
        os.system('mkdir data/' + hashtags[i][1:])

command_list = []
for i in range(len(hashtags)):
    delta = timedelta(days=(7-1))
    cycle = 1
    start_date_cycle = start_date

    while start_date_cycle <= until_date:
        # make sure the next cycle not exceed the until date
        if start_date_cycle + delta < until_date:
            until_date_cycle = start_date_cycle + delta
        else:
            until_date_cycle = until_date
        
        cycle_command = 'snscrape twitter-search' + ' "' + \
            hashtags[i]+' since:' + str(start_date_cycle) + ' until:' + str(until_date_cycle) + \
            ' filter:images" > data/' + hashtags[i][1:]+'/tweets' + str(cycle) + '.txt'
        command_list.append(cycle_command)

        # add 7 days to circle
        start_date_cycle += delta + timedelta(days=1)
        cycle += 1

with open('commands.txt', 'w') as f:
    for item in command_list:
        f.write("%s\n" % item)

file1 = open('commands.txt', 'r')
command_list = file1.readlines()
# print(command_list)
for i in command_list:
    print(i)
    os.system(i)
