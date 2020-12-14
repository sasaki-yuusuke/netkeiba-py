import requests
from bs4 import BeautifulSoup
import time

def request(url):
  time.sleep(1)

  res = requests.get(url)
  # https://virtualsanpo.blogspot.com/2020/01/pythonbeautifulsoup.html
  soup = BeautifulSoup(res.content.decode("euc-jp", "ignore"), 'html.parser')

  # print(soup.original_encoding)
  return soup