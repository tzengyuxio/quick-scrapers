#!/usr/bin/env python3
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os
import sys

import dataset
import requests
from datetime import date, timedelta

SQLITE_DB_URL = 'sqlite:///data/baha_rank.db'


def is_processed(date_str):
    if not os.path.exists('./data'):
        os.makedirs('./data')
    db = dataset.connect(SQLITE_DB_URL)
    table = db['baha_rank_mobile']
    info = table.find_one(date=date_str)
    return info is not None


def fetch_rank_page(page_no):
    url = 'https://forum.gamer.com.tw/ajax/rank.php?c=94&page={}'.format(page_no)
    r = requests.get(url)
    games = json.loads(r.text)
    return games


def save_rank_page(infos, date_str):
    db = dataset.connect(SQLITE_DB_URL)
    table = db['baha_rank_mobile']
    print('排名, (bsn)遊戲, (昨日人氣, 昨日文章)')
    for g in game_infos:
        row = {'date': date_str}
        row.update(g)
        table.insert(row)
        print('[{:03d}] ({}){} ({}/{})'.format(g['ranking'], g['bsn'], g['title'], g['hot'], g['article']))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    yesterday = (date.today() + timedelta(days=-1)).isoformat()  # 2020-08-29
    if is_processed(yesterday):
        sys.exit(0)
    game_infos = []
    for i in range(10):
        game_infos.extend(fetch_rank_page(i + 1))
    save_rank_page(game_infos, yesterday)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
