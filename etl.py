import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """ This process_song_file function reads the song file from the given filepath """
    df = pd.read_json(filepath, lines =True)

    """ This step Parses the required field from dataframe as per song data table and insert records into table"""
    song_data = df[["song_id","title", "artist_id", "year","duration"]].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    """ This step Parses the required field from dataframe as per artist data table and insert records into table"""
    artist_data = df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """ This process_log_file function reads the log file from the given filepath """
    df = pd.read_json(filepath, lines =True)

    """ This step filters the dataframe based on Page """
    df =  df[df.page=="NextSong"]

    """ This step converts the timestamp column to timestamp """
    t = pd.to_datetime(df['ts'], unit='ms')
    
    """ This step Parses the required field from dataframe as per time data table and insert records into table"""
    time_data = list((t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday))
    column_labels = list(("start_time", "hour", "day", "week", "month", "year", "weekday"))
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels,time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    """ This step Parses the required field from dataframe as per users data table and insert records into table"""
    user_df = df[['userId', 'firstName','lastName','gender', 'level']]

    
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    """This steps inserts the data into song play table"""
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (index, pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId,row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """ Getting files ending with .json and getting all the relative path """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    """ Iterating over each file and inserting as per required """
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()