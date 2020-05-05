Data Modeling using postgres

Sparkify Analytics

As the trend of custom recommended playlist increases. We are startup group who wants to fullfil their customers needs to provide enhanced and best recommended music playlist according to their mood and category for our customers via music streaming app.

The process started when we started to analyze our users activity, to know them better what kind of songs they listen and construct a real time ETL Workflow, which will parse, analyze, aggregate and Insert data into Postgres Database which will help us in categorizing and enhancing our recommendation models for our customer.

As mention we have two Data sources:
    1) Songs Data File
    2) Users Log Data
    
We have distributed our databases in form of STAR schema, for better analysis. The list of tables and their fiels are as follows:

Fact Table, also known as songplays table will contain records from log data associated with the songs such as:

    songplay_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP,
    user_id INTEGER,
    level VARCHAR(10),
    song_id VARCHAR(20),
    artist_id VARCHAR(20),
    session_id INTEGER,
    location VARCHAR(50),
    user_agent VARCHAR(150)


Dimension Tables design have been categorized as follows:

    1) Users Table - To get all the users from music streaming app, the respective schema for the table is attached below
        
        user_id INTEGER PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        gender CHAR(1),
        level VARCHAR(10)
        
    2) Songs Table - Collections of songs from music database, the respective schema for the table is attached below
        
        song_id VARCHAR(20) PRIMARY KEY,
        title VARCHAR(100),
        artist_id VARCHAR(20) NOT NULL,
        year INTEGER,
        duration FLOAT(5)
    
    3) Artist Table - Collections of artists from music database, the respective schema for the table is attached below
        
        artist_id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(100),
        location VARCHAR(100),
        lattitude FLOAT(5),
        longitude FLOAT(5)
    
    4) Time Table - Timestamps of song records played by the user which partitioned by year, month,.etc, the respective schema for the table is attached below
        
        start_time TIMESTAMP PRIMARY KEY,
        hour INTEGER,
        day INTEGER,
        week INTEGER,
        month INTEGER,
        year INTEGER,
        weekday INTEGER
        
The Project Structure is as follows:

    data - The directory where song_data and log_data JSOn file resides.
    sql_queries.py - contains all the sql queries which is utilized in create_tables.py and etl.py python files.
    create_tables.py -  This file contains python code to drop tables, create tables and insert records into the database and tables.
    etl.ipynb - This is a python notebook to read, parse and analyze single file from log_data and song_data into database.
    etl.py - This file contains python code to read, parse and insert data into the database by reading data files from the /data directory.
    test.ipynb - It is a python notebooks used to perform tests on the ingested data, to maintain data integrity.

Project Steps:

    1) Write sql queries for create, Insert and drop tables into sql_queries.py file and save it.
    2) Open console and run create_tables.py file, it will create Database, drop exisiting tables, create new tables for the project.
    3) Open etl.ipynb notebook and execute step by step to ingest one file of song_data and log_data into database and tables.
    4) Open etl.py file and edit as per etl.ipynb step by step to ingest all the data into database and tables.
    5) Open console and run etl.py file to ingest data into database and tables.
    6) Run test.ipynb to check the results and data integrity.
    
    Note: Before running etl.py or test.ipynb, make sure to edit sql_queries.py file if needed and run create_tables.py file to drop and create new tables.
    
ETL Pipeline Logic:

    1) Make sure you have created Databases, Tables and tested the connection to sparkifydb database.
    2) First, we will load the song_data JSON file into a dataframe using python pandas module.
    3) We will populate  song table and artist table by passing file to process_song_file function which will extract required fields and store into tables.
    4) Similarly to populate users and time table, we will use process_log_file function which will extract required fields from log_data JSON file and store into tables.
    5) Process_log_File functions filters data based on page where page is set to NextSong, Later the same the functions converts timestamp column to timestamp datatype.
    6) At last we are applying business logic. Since the log file does not specify an ID for either the song or the artist, we'll need to get the song ID and artist ID by          querying the songs and artists tables to find matches based on song title, artist name, and song duration time.
    7) The logic will be in the form of sql query and it's need to be written into sql_queries.py file.
    8) After successful ingestion, run test.ipynb notebook to run the test cases to maintain data integrity.

REMEMBER: since you can't make multiple connections to the same database.
Each time you run any notebook,remember to restart the notebook to close the connection to your database. Otherwise, you won't be able to run your code in create_tables.py, etl.py, or etl.ipynb files since you can't make multiple connections to the same database.

Author:
Devansh Modi
