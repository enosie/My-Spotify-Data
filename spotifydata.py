import pandas as pd
import requests
import json 
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import datetime
import sqlite3


USER_ID = '3nos3'
DATABASE_LOCATION = 'sqlite://my_recent_songs.sqlite'
TOKEN = 'BQBrQPJgNtPXwwA0UWAevx0_ffiHXBKA5ZYAxaW4dz4JhM2VycoL_JHJI7qQZxvw5AebvJrRDw9UZceCu80u-YIsTuX_zAVmY6owxtxEvlmM0HPlvRIQXxNU646dnLDuBk5IsSnV1IGGMQ'


if __name__ == '__main__':
  headers = {
    'Accept' : 'Application/json',
    'Content-Type': 'application/json',
    'Authorization' : 'Bearer {token}'.format(token=TOKEN)
  }

  today = datetime.datetime.now()
  yesterday = today - datetime.timedelta(days=1)
  yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
 
  r = requests.get('https://api.spotify.com/v1/me/player/recently-played?after={time}'.format(time=yesterday_unix_timestamp), headers = headers)

  data = r.json()

  song_name = []
  artist_name = []
  played_at = []
  timestamp = []

  
