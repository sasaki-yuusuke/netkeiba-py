from bs4 import BeautifulSoup
import re
import csv
import argparse
import config
import os
import datetime
from dateutil.relativedelta import relativedelta
from lib.utils import requesthtml

def main():
  argparser = argparse.ArgumentParser()

  argparser.add_argument('--startym')
  argparser.add_argument('--months', type=int)

  args = argparser.parse_args()

  base_url = "https://db.netkeiba.com/?pid=race_top"

  req_date = datetime.date.today()
  req_url = base_url

  if args.startym is not None:
    y = int(args.startym[0:4])
    m = int(args.startym[4:6])
    stdate = datetime.date(y, m, 1)
    req_date = stdate
    req_url += '&date=' + args.startym + '01'
  
  i = 0

  # nヶ月分のレースカレンダーを走査
  while i < args.months:
    urls = []

    print(req_url)
    soup = requesthtml.request(req_url)

    urllist = soup.find('div', class_='race_calendar').find_all('a', href=re.compile("/race/list/\\d+/"))

    # 開催日分のURLを取得しておく
    for link_tag in urllist:
      res = config.get('base_url') + link_tag.get('href')
      print(res)
      urls.append(res)

    prev_url = soup.select_one('img[src$="race_calendar_rev_02.gif"]').parent.get('href')
    print(prev_url)
    req_url = config.get('base_url') + prev_url
    print(req_url)
    i += 1

    for url in urls:
      datestr = url.lstrip(config.get('base_url') + '/race/list/').rstrip('/')
      path = 'data/urlcsv/' + datestr + '.csv'

      if os.path.exists(path):
        continue

      race_urls = []

      s = requesthtml.request(url)

      racelist = s.find('div', class_='race_list').find_all('a', href=re.compile("/race/\\d+/"))

      for tag in racelist:
        l = [config.get('base_url') + tag.get('href')]
        print(l)
        race_urls.append(l)

      with open(path, 'w', encoding="utf-8") as f:
        writer = csv.writer(f)
        # print(race_urls)
        writer.writerows(race_urls)

    req_date -= relativedelta(months=1)

if __name__ == "__main__":
  main()
