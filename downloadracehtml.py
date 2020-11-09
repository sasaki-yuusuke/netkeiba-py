from bs4 import BeautifulSoup
import re
import csv
from lib.utils import requesthtml

def main():
  with open('urlcollection.csv', 'r', encoding="utf-8") as f:
    reader = csv.reader(f)

    for row in reader:
      race_url = row[0]
      soup = requesthtml.request(race_url)
      race_path = re.search("/race/\\d+/", race_url).group()

      race_id = re.search(r'\d+', race_path).group()
      print(race_id)

      with open('html/' + race_id + '.html', mode = 'w', encoding = 'utf-8') as htmlf:
        htmlf.write(soup.prettify())


if __name__ == "__main__":
  main()
