CREATE_DATABASE = '''
  CREATE DATABASE keiba_db OWNER keibauser;
  '''

CREATE_RACEINFOS_TABLE = '''
  CREATE TABLE IF NOT EXISTS raceinfos(
    race_id char(12),
    year numeric(4,0),
    course_id char(2),
    course_round numeric(2,0),
    course_roundday numeric(2,0),
    race_num numeric(2,0),
    race_name varchar(60),
    is_turf numeric(1,0),
    is_dart numeric(1,0),
    is_jump numeric(1,0),
    distance numeric(4,0),
    course varchar(15),
    race_class varchar(15),
    race_condition varchar(20),
    weather varchar(10),
    ground_condition varchar(10),
    start_3f numeric(4,1),
    finish_3f numeric(4,1),
    race_datetime timestamp,
    PRIMARY KEY(race_id)
  );
  '''

CREATE_RACELAPS_TABLE = '''
  CREATE TABLE IF NOT EXISTS racelaps(
    race_id char(12),
    lap_start_point numeric(4,0),
    lap_time numeric(4,1),
    lap_distance numeric(4,0),
    PRIMARY KEY(race_id, lap_start_point)
  )
  '''

CREATE_RACERESULTS_TABLE = '''
  CREATE TABLE IF NOT EXISTS raceresults(
    race_id char(12),
    horse_num numeric(2,0),
    frame_num numeric(1,0),
    horse_id char(10),
    horse_name varchar(20),
    rank numeric(2,0),
    is_pulled_up numeric(1,0),
    is_disqualified numeric(1,0),
    is_scratched numeric(1,0),
    is_demoted numeric(1,0),
    is_retrained numeric(1,0),
    sex numeric(1,0),
    age numeric(2,0),
    jochey_id char(5),
    jockey_name varchar(30),
    jockey_weight numeric(3,1),
    goal_time numeric(4,1),
    goal_diff varchar(20),
    goal_time_diff numeric(4,1),
    speed_index numeric(3,0),
    finish_3f numeric(4,1),
    rank_pass varchar(20),
    remarks varchar(20),
    odds numeric(5,1),
    horse_weight numeric(3,0),
    trainer_id char(5),
    trainer varchar(30),
    owner_id char(6),
    owner varchar(30),
    PRIMARY KEY(race_id, horse_num)
  )
  '''

CREATE_COURSES_TABLE = '''
  CREATE TABLE IF NOT EXISTS courses(
    course_id char(2),
    course varchar(10),
    PRIMARY KEY(course_id)
  );
  '''

CREATE_HORSES_TABLE = '''
  CREATE TABLE IF NOT EXISTS horses(
    horse_id char(10),
    horse_name varchar(20),
    is_from_race numeric(1,0),
    birthday date,
    breeding_area varchar(20),
    sire_id char(10),
    sire_name varchar(20),
    dam_id char(10),
    dam_name varchar(20),
    broodmaresire_id char(10),
    broodmaresire_name varchar(20),
    coat_color varchar(5),
    trainer_id char(5),
    trainer varchar(30),
    trainer_area varchar(5),
    owner_id char(6),
    owner varchar(30),
    breeder_id char(6),
    breeder varchar(30),
    trade_price numeric(6,0),
    traded_auction varchar(20),
    earning_jra numeric(6,0),
    earning_nar numeric(6,0),
    total_races numeric(2,0),
    total_wins numeric(2,0),
    total_results varchar(12),
    PRIMARY KEY(horse_id)
  )
  '''
