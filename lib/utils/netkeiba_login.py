import requests
import os
from dotenv import load_dotenv

# https://pypi.org/project/python-dotenv/
load_dotenv()

def login_session():
  session = requests.Session()
  login_data = {
    'pid':'login',
    'action':'auth',
    'login_id':os.getenv('NETKEIBA_LOGIN_ID'),
    'pswd':os.getenv('NETKEIBA_PWD')
  }

  session.post('https://regist.netkeiba.com/account/', data=login_data)

  return session
