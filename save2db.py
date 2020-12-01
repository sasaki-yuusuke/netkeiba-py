from bs4 import BeautifulSoup
import glob
import re
import os
import psycopg2
from decimal import Decimal
from datetime import datetime
from lib.app import init_db

html_files = glob.glob("./html/*.html")

initdb = init_db.InitDb()
initdb.execute()

for filename in html_files:
  print(filename)
  race_id = filename.strip('./html/').strip('.html')
  print(race_id)
  year = race_id[0:4]
  course_id = race_id[4:6]
  course_round = race_id[6:8]
  course_roundday = race_id[8:10]
  race_num = race_id[10:]
  soup = BeautifulSoup(open(filename), 'html.parser')

  # print(soup.find('div', class_='mainrace_data fc'))
  race_info = soup.find('div', class_='mainrace_data')
  
  race_name = race_info.find('h1').get_text().strip()
  print(race_name.strip())

  race_cond = race_info.find('p').find('diary_snap_cut').find('span')
  race_cond_txt = race_cond.get_text()
  # print(race_cond_txt)
  race_cond_list = race_cond_txt.split('/')

  course = race_cond_list[0].strip()
  is_turf = is_dart = is_jump = 0
  if '障' in course:
    is_jump = 1
  elif 'ダ' in course:
    is_dart = 1
  elif '芝' in course:
    is_turf = 1
  else:
    raise ValueError('コース条件の例外：'+ course)
  distance = re.findall('(\\d+)m', course.strip())[0]
  print(distance)

  weather = race_cond_list[1].strip().replace('天候 : ', '')
  print(weather)

  ground_cond = race_cond_list[2].strip().split(':')[1].strip()
  print(ground_cond)

  start_time = race_cond_list[3].strip().replace('発走 : ', '')
  print(start_time)

  race_outline = race_info.find('p', class_='smalltxt')
  race_outline_txt = race_outline.get_text()
  race_outline_list = race_outline_txt.strip().split(' ')

  race_date = datetime.strptime(race_outline_list[0] + '_' + start_time, "%Y年%m月%d日_%H:%M")
  print(race_date)
  race_cond_txt = race_outline_list[2]
  print(race_cond_txt)
  race_cond_list = race_cond_txt.split(u'\xa0')
  race_class = race_cond_list[0]
  print(race_class)
  race_cond = race_cond_list[2]


  con = psycopg2.connect('postgresql://keibauser:QWEzxcvbnm1234@localhost/keiba_db')
  cur = con.cursor()


  lap_table = soup.find('table', class_='result_table_02', summary='ラップタイム')
  laps = lap_table.find_all('td', class_='race_lap_cell')
  if laps != []:
    lap_txt = laps[0].get_text().strip()
    lap_list = lap_txt.split(' - ')
    lap_start_point = int(distance)
    for lap in lap_list:
      lap_distance = 200 if lap_start_point % 200 == 0 else lap_start_point % 200
      racelap_param = [ race_id, lap_start_point, lap, lap_distance ]
      cur.execute("INSERT INTO racelaps VALUES (%s,%s,%s,%s)", racelap_param)
      lap_start_point -= lap_distance
      
    print(laps[0].get_text().strip())
    pace_re = re.search(r"(\()(.*?)\)", laps[1].get_text().strip())
    pace_txt = pace_re.group()
    pace_list = pace_txt.lstrip('(').rstrip(')').split('-')
    start_3f = pace_list[0]
    finish_3f = pace_list[1]

  raceinfo_param = [ race_id, year, course_id, course_round, course_roundday, race_num, race_name,
                     is_turf, is_dart, is_jump, distance, course, race_class, race_cond, weather, ground_cond, 
                     start_3f, finish_3f, race_date ]
  print(raceinfo_param)
  cur.execute("INSERT INTO raceinfos VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", raceinfo_param)

  race_results = soup.find('table', class_='race_table_01').find_all('tr')
  # race_results.find('tr', class_='txt_c').decompose()
  # print(race_results[1])
  # 1着馬の走破タイムを保持
  top_goal_time = None

  for tr in race_results:
    tds = tr.find_all('td')
    print('-------------')

    if tds != []:
      # 着順
      print('着順')
      rank_txt = tds[0].get_text().strip()
      rank_re = re.search(r'\d+', rank_txt)
      rank = rank_re.group() if not rank_re is None else None
      # 降着
      is_demoted = 1 if '(降)' in rank_txt else 0
      # 再調教？
      is_retrained = 1 if '(再)' in rank_txt else 0
      # 競走中止
      is_pulled_up = 1 if '中' in rank_txt else 0
      # 失格
      is_disqualified = 1 if '失' in rank_txt else 0
      # 出走取消／競走除外
      is_scratched = 1 if re.search('取|除', rank_txt) else 0
      print(tds[0].get_text().strip())

      # 枠番
      print('枠番')
      frame_num = tds[1].get_text().strip()
      print(tds[1].get_text().strip())

      # 馬番
      print('馬番')
      horse_num = tds[2].get_text().strip()
      print(tds[2].get_text().strip())

      # 馬名
      horse_link = tds[3].find('a').get('href')
      # /horse/¥¥d/
      horse_id = horse_link.split('/')[2]
      print(horse_id)
      horse_name = tds[3].get_text().strip()
      print(horse_name)

      # 性齢
      sex_age_txt = tds[4].get_text().strip()
      if '牡' in sex_age_txt:
        sex = 1
      elif '牝' in sex_age_txt:
        sex = 2
      else:
        sex = 3
      age = re.search(r'\d+', sex_age_txt).group()

      # 斤量
      jockey_weight = tds[5].get_text().strip()

      # 騎手
      jockey_link = tds[6].find('a').get('href')
      # /jockey/¥¥d/
      jockey_id = jockey_link.split('/')[2]
      jockey_name = tds[6].get_text().strip()

      # タイム
      goal_time_txt = tds[7].get_text().strip()
      if len(goal_time_txt) > 0:
        goal_time_array = tds[7].get_text().split(':')
        if len(goal_time_array) == 2:
          goal_time_min = Decimal(goal_time_array[0])
          goal_time_sec = Decimal(goal_time_array[1])
          goal_time = goal_time_min * 60 + goal_time_sec
        else:
          goal_time = Decimal(goal_time_array[0])
        top_goal_time = goal_time if int(rank) == 1 else top_goal_time
        goal_time_diff = goal_time - top_goal_time

      # 着差
      goal_diff = tds[8].get_text().strip()
      
      # タイム指数(P)
      # print(tds[9].get_text())

      # 通過順位
      rank_pass = tds[10].get_text().strip()

      # 上がり３F
      finish_3f_txt = tds[11].get_text().strip()
      finish_3f = finish_3f_txt if len(finish_3f_txt) > 0 else None

      # 単勝オッズ
      odds_txt = tds[12].get_text().strip()
      if not '-' in odds_txt:
        odds = odds_txt

      # 人気
      # print(tds[13].get_text())

      # 馬体重
      horse_weight_txt = tds[14].get_text().strip()
      if not '計不' in horse_weight_txt:
        horse_weight = horse_weight_txt.split('(')[0]
      # horse_weight = re.search(r'^(?!(\()(.*?)\))', horse_weight_txt).group() if not '計不' in horse_weight_txt else null
      # print(tds[14].get_text())

      # 調教タイム(P)
      # print(tds[15].get_text())

      # 厩舎コメント(P)
      # print(tds[16].get_text())

      # 備考(P)
      # print(tds[17].get_text())

      # 調教師
      trainer_link = tds[18].find('a').get('href')
      # /trainer/¥¥d/
      trainer_id = trainer_link.split('/')[2]
      trainer = tds[18].get_text().strip()
      # print(tds[18].get_text())

      # 馬主
      owner_link = tds[19].find('a').get('href')
      # /owner/¥¥d/
      owner_id = owner_link.split('/')[2]
      owner = tds[19].get_text().strip()
      # owner_base = owner_txt[0]
      # owner = owner_txt[2]
      # print(owner_txt)
      # print(owner_base)
      print(owner)

      # 賞金
      # print(tds[20].get_text())

      raceresult_param = [ race_id, horse_num, frame_num, horse_id, horse_name, rank,
                             is_pulled_up, is_disqualified, is_scratched, is_demoted, is_retrained,
                             sex, age, jockey_id, jockey_name, jockey_weight, goal_time, goal_diff, goal_time_diff,
                             finish_3f, rank_pass, odds, horse_weight,
                             trainer_id, trainer, owner_id, owner ]
      print(raceresult_param)
      cur.execute("INSERT INTO raceresults VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", raceresult_param)
      
  con.commit()
