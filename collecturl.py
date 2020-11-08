import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import argparse
import config.actionmode
from lib.utils import requesthtml

def main():
  base_url = "https://db.netkeiba.com/?pid=race_top"
  i = 0
  urls = []
  # 初回のリクエストはデータベースのトップページ。
  req_url = base_url

  # nヶ月分のレースカレンダーを走査
  while i < 3:
    soup = requesthtml.request(req_url)

    urllist = soup.find('div', class_='race_calendar').find_all('a', href=re.compile("/race/list/\\d+/"))

    # 開催日分のURLを取得しておく
    for link_tag in urllist:
      res = "https://db.netkeiba.com" + link_tag.get('href')
      print(res)
      urls.append(res)

    prev_url = soup.select_one('img[src$="race_calendar_rev_02.gif"]').parent.get('href')
    print(prev_url)
    req_url = "https://db.netkeiba.com" + prev_url
    print(req_url)
    i += 1

  race_urls = []

  for url in urls:
    s = requesthtml.request(url)

    racelist = s.find('div', class_='race_list').find_all('a', href=re.compile("/race/\\d+/"))

    for tag in racelist:
      l = ["https://db.netkeiba.com" + tag.get('href')]
      print(l)
      race_urls.append(l)

  with open('urlcollection.csv', 'w', encoding="utf-8") as f:
    writer = csv.writer(f)
    # print(race_urls)
    writer.writerows(race_urls)

if __name__ == "__main__":
  main()
