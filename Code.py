#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# USAGE:
#   python Lab1.py Sample_Song_Dataset.db

import sys
import sqlite3


# The database file should be given as the first argument on the command line
db_file = sys.argv[1]

# We connect to the database using 
with sqlite3.connect(db_file) as conn:
    cursor = conn.cursor()
    
    # This query counts the number of tracks from the year 1998
    year = ('1998',)
    cursor.execute('SELECT count(*) FROM tracks WHERE year=?', year)
    
    # Since there is no grouping here, the aggregation is over all rows
    # and there will only be one output row from the query, which we can
    # print as follows:
    print('Tracks from {}: {}'.format(year[0], cursor.fetchone()[0]))
    # The [0] bits here tell us to pull the first column out of the 'year' tuple
    # and query results, respectively.
    
    # ADD YOUR CODE STARTING HERE
    
    # 1. Find id, name and term of the artist who played the track with id TRMMWLD128F9301BF2
    cursor.execute('SELECT artists.artist_id, artists.artist_name, artist_term.term From artists JOIN artist_term on artists.artist_id = artist_term.artist_id JOIN tracks on tracks.artist_id = artists.artist_id WHERE tracks.track_id ="TRMMWLD128F9301BF2"')
    print(cursor.fetchall())
    
    # 2. Select all the unique tracks with the duration is strictly greater than 3020 seconds.
    cursor.execute('SELECT DISTINCT * FROM tracks WHERE duration>"3020"')
    print(cursor.fetchall())
    
    # 3. Find the ten shortest (by duration) 10 tracks released between 2010 and 2014 (inclusive), ordered by increasing duration.
    cursor.execute('SELECT * FROM tracks WHERE year BETWEEN "2010" AND "2014" ORDER BY duration LIMIT 10')
    print(cursor.fetchall())
    
    # 4. Find the top 20 most frequently used terms, ordered by decreasing usage.
    cursor.execute('SELECT term FROM artist_term GROUP BY term ORDER BY COUNT(*) DESC LIMIT 20')
    print(cursor.fetchall())
    
    # 5. Find the artist name associated with the longest track duration.
    #cursor.execute('SELECT artists.artist_name FROM artists JOIN tracks on tracks.artist_id = artists.artist_id ORDER BY tracks.duration DESC LIMIT 1')
    cursor.execute('SELECT artists.artist_name FROM artists JOIN tracks on tracks.artist_id = artists.artist_id WHERE duration=(SELECT MAX(duration) FROM tracks )')
    print(cursor.fetchall())
    
    # 6. Find the mean duration of all tracks.
    cursor.execute('SELECT AVG(duration) FROM tracks')
    print(cursor.fetchall())
    
    # 7. Using only one query, count the number of tracks whose artists don't have any linked terms.
    cursor.execute('SELECT COUNT(*) FROM tracks LEFT JOIN artist_term on tracks.artist_id = artist_term.artist_id WHERE artist_term.artist_id IS NULL')
    #cursor.execute('SELECT COUNT(*) FROM tracks WHERE tracks.artist_id NOT IN (SELECT artist_id FROM artist_term)')
    print(cursor.fetchall())
    
    # 8. Index- Run Question 1 query in a loop for 100 times and note the minimum time taken.
    # Now create an index on the column artist_id and compare the time. Share your findings in the report.
    import time
    start = time.time()
    for i in range(100):
        cursor.execute('SELECT artists.artist_id, artists.artist_name, artist_term.term From artists JOIN artist_term on artists.artist_id = artist_term.artist_id JOIN tracks on tracks.artist_id = artists.artist_id WHERE tracks.track_id ="TRMMWLD128F9301BF2"')
    end = time.time()
    print(end-start)
    
    cursor.execute('CREATE INDEX artist_id_index_tracks ON tracks (artist_id)')
    cursor.execute('CREATE INDEX artist_id_index_artists ON artists (artist_id)')
    cursor.execute('CREATE INDEX artist_id_index_artist_term ON artist_term (artist_id)')
    start1 = time.time()
    for i in range(100):
        cursor.execute('SELECT artists.artist_id, artists.artist_name, artist_term.term From artists JOIN artist_term on artists.artist_id = artist_term.artist_id JOIN tracks on tracks.artist_id = artists.artist_id WHERE tracks.track_id ="TRMMWLD128F9301BF2"')
    end1 = time.time()
    print(end1-start1)

    #9. Find all tracks associated with artists that have the tag eurovision winner and delete them from the database, then roll back this query using a transaction. Hint: you can select from the output of a select!
    cursor.execute('BEGIN TRANSACTION')
    cursor.execute('DELETE FROM tracks WHERE tracks.track_id IN (SELECT tracks.track_id FROM tracks JOIN artist_term on artist_term.artist_id = tracks.artist_id WHERE artist_term.term ="eurovision winner")')
    cursor.execute('ROLLBACK')
    print(cursor.fetchall())
