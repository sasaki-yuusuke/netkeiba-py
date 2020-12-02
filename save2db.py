from bs4 import BeautifulSoup
import glob
import os
import psycopg2
from lib.app import init_db
from lib.app import raceinfo
from lib.app import racelap
from lib.app import raceresult

html_files = glob.glob("./html/*.html")

init_db.InitDb().execute()

for filename in html_files:
  race_id = filename.strip('./html/').strip('.html')
  print(race_id)
  soup = BeautifulSoup(open(filename), 'html.parser')

  con = psycopg2.connect('postgresql://keibauser:QWEzxcvbnm1234@localhost/keiba_db')
  cur = con.cursor()

  raceinfo.Raceinfo().execute(race_id, soup, cur)

  racelap.Racelap().execute(race_id, soup, cur)

  raceresult.Raceresult().execute(race_id, soup, cur)

  con.commit()
