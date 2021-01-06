import requests

def login_session():
  session = requests.Session()
  login_data = {
    'pid':'login',
    'action':'auth',
    'login_id':'LOGINUSER',
    'pswd':'PASSWORD'
  }

  session.post('https://regist.netkeiba.com/account/', data=login_data)

  return session
