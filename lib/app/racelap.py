from bs4 import BeautifulSoup
import psycopg2
import re

class Racelap():

  def execute(self, race_id, soup, cursor):
    race_info = soup.find('div', class_='mainrace_data')
    
    race_cond = race_info.find('p').find('diary_snap_cut').find('span')
    race_cond_txt = race_cond.get_text()
    # print(race_cond_txt)
    race_cond_list = race_cond_txt.split('/')

    course = race_cond_list[0].strip()

    distance = re.findall('(\\d+)m', course.strip())[0]

    lap_table = soup.find('table', class_='result_table_02', summary='ラップタイム')
    laps = lap_table.find_all('td', class_='race_lap_cell')
    if laps != []:
      lap_txt = laps[0].get_text().strip()
      lap_list = lap_txt.split(' - ')
      lap_start_point = int(distance)
      for lap in lap_list:
        lap_distance = 200 if lap_start_point % 200 == 0 else lap_start_point % 200
        racelap_param = [ race_id, lap_start_point, lap, lap_distance ]
        cursor.execute("INSERT INTO racelaps VALUES (%s,%s,%s,%s,now(),now())", racelap_param)
        lap_start_point -= lap_distance