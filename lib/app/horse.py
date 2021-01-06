class Horse():
  def is_exist(self, horse_id, cursor):
    cursor.execute("SELECT COUNT(horse_id) FROM horses WHERE horse_id = %s", [horse_id])
    cnt_rcd = cursor.fetchone()
    return cnt_rcd[0] > 0
  
  def is_exist_from_race(self, horse_id, cursor):
    cursor.execute("SELECT COUNT(horse_id) FROM horses WHERE horse_id = %s and is_from_race = 1", [horse_id])
    cnt_rcd = cursor.fetchone()
    return cnt_rcd[0] > 0  
