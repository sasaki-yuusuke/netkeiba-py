from bs4 import BeautifulSoup
import re
import os
import glob
import csv
from lib.utils import requesthtml

def main():
  csv_file_paths = glob.glob("./data/urlcsv/*.csv")

  for csv_path in csv_file_paths:
    directory_name = os.path.basename(csv_path).rstrip(".csv")

    if os.path.exists('data/html/' + directory_name):
      continue
    else:
      os.makedirs('data/html/' + directory_name)

    with open(csv_path, 'r', encoding="utf-8") as f:
      reader = csv.reader(f)

      for row in reader:
        race_url = row[0]
        soup = requesthtml.request(race_url)
        race_path = re.search("/race/\\d+/", race_url).group()

        race_id = re.search(r'\d+', race_path).group()
        print(race_id)

        with open('data/html/' + directory_name + '/' + race_id + '.html', mode = 'w', encoding = 'utf-8') as htmlf:
          htmlf.write(soup.prettify())


if __name__ == "__main__":
  main()
