import requests
from bs4 import BeautifulSoup
import time

# 単発のHTTPリクエスト（ログインなし）
def request(url):
  time.sleep(1)

  res = requests.get(url)
  # https://virtualsanpo.blogspot.com/2020/01/pythonbeautifulsoup.html
  soup = BeautifulSoup(res.content.decode("euc-jp", "ignore"), 'html.parser')

  # print(soup.original_encoding)
  return soup

# ログインセッションを維持した状態でのHTTPリクエスト
# https://qiita.com/mSpring/items/257adb27d9170da3b372
def request_with_login(url, session):
  time.sleep(1)

  res = session.get(url)
  # https://virtualsanpo.blogspot.com/2020/01/pythonbeautifulsoup.html
  soup = BeautifulSoup(res.content.decode("euc-jp", "ignore"), 'html.parser')

  # print(soup.original_encoding)
  return soup