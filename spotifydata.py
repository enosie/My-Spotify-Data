import pandas as pd
import requests
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import datetime
import sqlite3

#somehow find a way to get a longer lasting token, constant change is annoying
USER_ID = '3nos3'
DATABASE_LOCATION = 'sqlite://my_recent_songs.sqlite'
TOKEN = 'BQDQPc9ZXpdhmEiEMCrf3WRISxbtD2aWBG0NjPDvsAdFE_VH750Hcvgev0piYyCA2hwkmZY0LOGAvZqCaI6olMJ0Q47X48EdgYuKZxuiyN3eP6pCnlFF2P1N9qmBEejQ32dvTm-klHGFBH7brbII6S_4iogrcbApUefdSTdRYD5jfPACHkYR2sDbNbanSAm-PHsbO1zGEwWzKVMXU60bJ0KUbCtPICa2aAh1SpklCYZdNirdugjlV5u3tH74dLNLyCBdqxZ4dUovvtFGBg'


def check_valid_data(df: pd.DataFrame) -> bool:
    if df.empty:
        print('No songs played.')
        return False

    if pd.Series(df['playedAt']).is_unique:
        pass
    else:
        raise Exception('Primary Key Check is Violated')

    if df.isnull().values.any():
        raise Exception('Null Value(s)')

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps = df["timestamp"].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
            raise Exception(
                "At least one of the returned songs does not have a yesterday's timestamp")

    return True


if __name__ == '__main__':
    headers = {
        'Accept': 'Application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {token}'.format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get('https://api.spotify.com/v1/me/player/recently-played?after={time}'.format(
        time=yesterday_unix_timestamp), headers=headers)

    data = r.json()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song['track']['name'])
        artist_names.append(song['track']['album']['artists'][0]['name'])
        played_at_list.append(song['played_at'])
        timestamps.append(song['played_at'][0:10])

    song_dict = {
        'songName': song_names,
        'artistName': artist_names,
        'playedAt': played_at_list,
        'timestamp': timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=[
                           'songName', 'artistName', 'playedAt', 'timestamp'])

print(song_df)