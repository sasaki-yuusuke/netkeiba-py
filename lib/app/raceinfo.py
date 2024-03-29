from bs4 import BeautifulSoup
import psycopg2
import re
from datetime import datetime

class Raceinfo():

  def is_exist(self, race_id, cursor):
    cursor.execute("SELECT COUNT(race_id) FROM raceinfos WHERE race_id = %s", [race_id])
    cnt_rcd = cursor.fetchone()
    return cnt_rcd[0] > 0

  def execute(self, race_id, soup, cursor):
    year = race_id[0:4]
    course_id = race_id[4:6]
    course_round = race_id[6:8]
    course_roundday = race_id[8:10]
    race_num = race_id[10:]

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

    weather = race_cond_list[1].strip().replace('天候 : ', '')

    ground_cond = race_cond_list[2].strip().split(':')[1].strip()

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

    is_juvenile = is_only3yearold = 0
    if race_class.startswith('2歳'):
      is_juvenile = 1
    if race_class.startswith('3歳') and '3歳以上' not in race_class:
      is_only3yearold = 1

    is_openclass = 0
    if race_class.endswith('オープン'):
      is_openclass = 1
      if race_name.endswith('L'):
        grade = 11
      elif race_name.endswith('G'):
        grade = 12
      elif race_name.endswith('G3)'):
        grade = 13
      elif race_name.endswith('G2)'):
        grade = 14
      elif race_name.endswith('G1)'):
        grade = 15
      else:
        grade = 10
    else:
      if race_class.endswith('新馬'):
        grade = 0
      elif race_class.endswith('3勝クラス'):
        grade = 7
      elif race_class.endswith('1600万下'):
        grade = 6
      elif race_class.endswith('2勝クラス'):
        grade = 5
      elif race_class.endswith('1000万下'):
        grade = 4
      elif race_class.endswith('1勝クラス'):
        grade = 3
      elif race_class.endswith('500万下'):
        grade = 2
      elif race_class.endswith('未勝利'):
        grade = 1
      else:
        raise ValueError('レース格の例外: ' + race_class)

    race_cond = race_cond_list[2]

    lap_table = soup.find('table', class_='result_table_02', summary='ラップタイム')
    laps = lap_table.find_all('td', class_='race_lap_cell')
    start_3f = None
    finish_3f = None
    if laps != []:
      pace_re = re.search(r"(\()(.*?)\)", laps[1].get_text().strip())
      pace_txt = pace_re.group()
      pace_list = pace_txt.lstrip('(').rstrip(')').split('-')
      start_3f = pace_list[0]
      finish_3f = pace_list[1]

    raceinfo_param = [ race_id, year, course_id, course_round, course_roundday, race_num, race_name,
                      is_turf, is_dart, is_jump, distance, course, race_class, race_cond, weather, ground_cond, 
                      start_3f, finish_3f, race_date, is_juvenile, is_only3yearold, grade, is_openclass]
    print(raceinfo_param)
    cursor.execute("INSERT INTO raceinfos VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now())", raceinfo_param)
