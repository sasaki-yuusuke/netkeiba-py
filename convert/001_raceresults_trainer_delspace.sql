-- 調教師列　の改行コードおよび空白を削除
UPDATE raceresults
SET trainer = REGEXP_REPLACE(trainer, '\n         ', '', 'g');