from bs4 import BeautifulSoup
import psycopg2
import re
from decimal import Decimal

class Raceresult():

  def execute(self, race_id, soup, cursor):
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
        cursor.execute("INSERT INTO raceresults VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", raceresult_param)
        