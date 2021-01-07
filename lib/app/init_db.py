import psycopg2
from lib.sqls import create_state
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class InitDb():
  def execute(self):
    self.create_db()
    self.create_tables()
  
  def create_db(self):
    # dsn = 'postgresql://{username}:{password}@{hostname}:'
    dsn = 'postgresql://keibauser:QWEzxcvbnm1234@localhost:'
    conn = psycopg2.connect(dsn)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM pg_database WHERE datname='keiba_db');")

    if not cur.fetchone()[0]:
      cur.execute(create_state.CREATE_DATABASE)


  def create_tables(self):
    dsn = 'postgresql://keibauser:QWEzxcvbnm1234@localhost/keiba_db'
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    self.create_raceinfos_table(cur)
    self.create_racelaps_table(cur)
    self.create_raceresults_table(cur)
    self.create_courses_table(cur)
    self.create_horses_table(cur)

    self.copy_courses_initdata(cur)
    cur.close()
    conn.commit()
  
  def create_raceinfos_table(self, cur):
    cur.execute(create_state.CREATE_RACEINFOS_TABLE)
  
  def create_racelaps_table(self, cur):
    cur.execute(create_state.CREATE_RACELAPS_TABLE)
  
  def create_raceresults_table(self, cur):
    cur.execute(create_state.CREATE_RACERESULTS_TABLE)

  def create_courses_table(self, cur):
    cur.execute(create_state.CREATE_COURSES_TABLE)

  def create_horses_table(self, cur):
    cur.execute(create_state.CREATE_HORSES_TABLE)


  def copy_courses_initdata(self, cur):
    """
    coursesテーブルの初期データ投入（COPYコマンドを利用してCSVからデータ投入）

    Parameters
    ----------
    cur : psycopg2.cursor
      psycopg2のカーソルオブジェクト
    """

    cur.execute("SELECT COUNT(course_id) FROM courses")
    cnt_rcd = cur.fetchone()
    return cnt_rcd[0] > 0

    path = './db/seeds/courses.csv'
    copy_sql = '''
      COPY courses FROM stdin WITH CSV HEADER
           DELIMITER as ','
      '''

    with open(path, 'r') as f:
      cur.copy_expert(sql=copy_sql, file=f)
