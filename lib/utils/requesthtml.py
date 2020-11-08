import requests
from bs4 import BeautifulSoup
import time

def request(url):
  time.sleep(1)

  res = requests.get(url)
  return BeautifulSoup(res.content, 'html.parser')