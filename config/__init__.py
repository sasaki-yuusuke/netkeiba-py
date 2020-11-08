import yaml

# https://teratail.com/questions/45746
class ConfigUtil:

  def __init__(self):
    with open('./config/settings.yml', 'r') as file:
      self.config = yaml.safe_load(file)

_util = ConfigUtil()

def get(key):
  return _util.config[key]

