alter table raceinfos add column is_juvenile numeric(1,0) default 0;
alter table raceinfos add column is_only3yearold numeric(1,0) default 0;
alter table raceinfos add column grade numeric(2,0);
alter table raceinfos add column is_openclass numeric(1,0) default 0;


update raceinfos set is_juvenile = 1 where race_class like '2歳%';
update raceinfos set is_only3yearold = 1 where race_class like '3歳%' and race_class not like '%3歳以上%';


update raceinfos set grade = 10 where race_class like '%オープン';
update raceinfos set grade = 11 where race_name like '%(L)' and race_class like '%オープン';
update raceinfos set grade = 12 where race_name like '%(G)' and race_class like '%オープン';
update raceinfos set grade = 13 where race_name like '%G3)' and race_class like '%オープン';
update raceinfos set grade = 14 where race_name like '%G2)' and race_class like '%オープン';
update raceinfos set grade = 15 where race_name like '%G1)' and race_class like '%オープン';
update raceinfos set is_openclass = 1 where race_class like '%オープン';

update raceinfos set grade = 0 where race_class like '%新馬' and grade isnull;
update raceinfos set grade = 7 where race_class like '%3勝クラス' and grade isnull;
update raceinfos set grade = 6 where race_class like '%1600万下' and grade isnull;
update raceinfos set grade = 5 where race_class like '%2勝クラス' and grade isnull;
update raceinfos set grade = 4 where race_class like '%1000万下' and grade isnull;
update raceinfos set grade = 3 where race_class like '%1勝クラス' and grade isnull;
update raceinfos set grade = 2 where race_class like '%500万下' and grade isnull;
update raceinfos set grade = 1 where race_class like '%未勝利' and grade isnull;