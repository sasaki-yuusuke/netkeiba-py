from bs4 import BeautifulSoup
import os
import glob
import argparse
import requests
import psycopg2
from lib.app import horse
from lib.utils import requesthtml, netkeiba_login

argparser = argparse.ArgumentParser()

argparser.add_argument('--year')
argparser.add_argument('--course_id')

args = argparser.parse_args()

html_files = glob.glob("./data/racehtml/*/*.html")

con = psycopg2.connect('postgresql://keibauser:QWEzxcvbnm1234@localhost/keiba_db')
cursor = con.cursor()

for filename in html_files:
  race_id = os.path.basename(filename).rstrip('.html')
  print(race_id)

  year = race_id[0:4]
  course_id = race_id[4:6]
  course_round = race_id[6:8]
  course_roundday = race_id[8:10]
  race_num = race_id[10:]

  if args.year != year:
    continue

  if args.course_id != course_id:
    continue

  print(filename)
  print(os.path.isfile(filename))

  soup = BeautifulSoup(open(filename), 'html.parser')

  race_results = soup.find('table', class_='race_table_01').find_all('tr')

  for tr in race_results:
    tds = tr.find_all('td')

    if tds == []:
      continue

    # 馬名
    horse_link = tds[3].find('a').get('href')
    # /horse/¥¥d/
    horse_id = horse_link.split('/')[2]
    print(horse_id)
    horse_name = tds[3].get_text().strip()
    print(horse_name)

    # 一旦、既にHTMLがあればスキップする
    if os.path.isfile('data/horsehtml/' + horse_id + '.html'):
      continue

    # racehtmlから既に登録済みの馬ならスキップ
    if horse.Horse().is_exist_from_race(horse_id, cursor):
      continue

    # is_from_race = 0で既に登録済みのケース。
    if horse.Horse().is_exist(horse_id, cursor):
      # is_from_race = 1にUPDATE
      continue

    # 
    if not os.path.exists('data/horsehtml'):
      os.makedirs('data/horsehtml')
    
    # netkeibaへのログイン処理
    session = netkeiba_login.login_session()

    horse_url = "https://db.netkeiba.com/horse/" + horse_id
    print(horse_url)
    s = requesthtml.request_with_login(horse_url, session)

    with open('data/horsehtml/' + horse_id + '.html', mode = 'w', encoding = 'utf-8') as htmlf:
      htmlf.write(s.prettify())
    

    