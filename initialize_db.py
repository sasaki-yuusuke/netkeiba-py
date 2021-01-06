from lib.app import init_db

def main():
  init_db.InitDb().execute()

if __name__ == "__main__":
  main()