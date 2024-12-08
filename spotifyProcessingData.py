import json
import pandas as pd
from collections import Counter
import numpy as np
from prettytable import PrettyTable
import glob
import os

# establish which files should be used
directory = os.getcwd() +'/Spotify Extended Streaming History'
filenames = [directory + '/' + filename for filename in os.listdir(directory)if filename.endswith('json')]
data = []

# open all files
for filename in filenames:
    with open(filename, 'r') as file:
        datai = json.load(file)
    data = data + datai

# choose what year to look at from all data
data = [dataPoint for dataPoint in data if dataPoint['ts'].startswith("2024")]

# get all songs played and their play times and artists - essentially simplify the data to what we want to analyse
allSongs = []
playTime = []
artist = []
totalListeningMin = 0;
for dataPoint in data:
    allSongs = allSongs + [dataPoint['master_metadata_track_name']]
    playTime = playTime + [dataPoint['ms_played']]
    artist = artist + [dataPoint['master_metadata_album_artist_name']]
    totalListeningMin = totalListeningMin + dataPoint['ms_played']

totalListeningMin = round((totalListeningMin)/60000)
print('total listening time: ' + str(totalListeningMin))

#convert to an array
songsAndPT = [allSongs, playTime, artist]
songsAndPT = np.array(songsAndPT)
songsAndPT = songsAndPT[:, np.where(songsAndPT[0] != None)[0]]

# find the total play times for each unique song and sort from most to least
uniqueSongs, counts = np.unique(songsAndPT[0], return_counts=True) # find unique songs
mostPlayedData = [] #initialize lists
for songTitle in uniqueSongs:
    indicies = np.where((songsAndPT[0] == songTitle)&(songsAndPT[1]>= 30000)) # find where the song was played
    numberOfPlays = len(indicies[0])
    if numberOfPlays != 0:
        artist = songsAndPT[2][indicies[0][0]]
        totalPT = sum(songsAndPT[1][indicies[0]]) # find total play time
        dataPoint = (songTitle, numberOfPlays, totalPT, artist)
        mostPlayedData = mostPlayedData+ [dataPoint] #store
dtype = [('songTitle', 'U40'), ('plays', int), ('totalPlayTime', int), ('artist', 'U40')]
mostPlayedData = np.array(mostPlayedData, dtype=dtype) #convert to array
mostPlayedCount = np.sort(mostPlayedData, order='plays')[::-1]
mostPlayedTime = np.sort(mostPlayedData, order='totalPlayTime')[::-1]


# get top 5 songs
mostPlayedCount = mostPlayedCount[:5]
mostPlayedTime = mostPlayedTime[:5]

displaytable = PrettyTable()
displaytable.add_column("Song Title", mostPlayedCount['songTitle'])
displaytable.add_column("Artist", mostPlayedCount['artist'])
displaytable.add_column("Number of Plays", mostPlayedCount['plays'])
displaytable.add_column("Total Play Time", np.round(mostPlayedCount['totalPlayTime']/60000, 1))
print('2024 Top Songs by Number of Plays')
print(displaytable)

displaytable = PrettyTable()
displaytable.add_column("Song Title", mostPlayedTime['songTitle'])
displaytable.add_column("Artist", mostPlayedTime['artist'])
displaytable.add_column("Number of Plays", mostPlayedTime['plays'])
displaytable.add_column("Total Play Time", np.round(mostPlayedTime['totalPlayTime']/60000, 1))
print('2024 Top Songs by Play Time')
print(displaytable)

del displaytable
del mostPlayedCount
del mostPlayedTime

### --------- ARTISTS --------- ###

# find top 5 artists (analagous to top 5 songs)
uniqueArtists, counts = np.unique(songsAndPT[2], return_counts=True) # find unique songs
mostPlayedData = []
for artist in uniqueArtists:
    indicies = np.where((songsAndPT[2] == artist)&(songsAndPT[1]>= 30000)) # find where the artist was played
    numberOfPlays = len(indicies[0])
    if numberOfPlays != 0:
        totalPT = sum(songsAndPT[1][indicies[0]]) # find total play time
        dataPoint = (artist, numberOfPlays, totalPT)
        mostPlayedData = mostPlayedData+ [dataPoint] #store
dtype = [('artist', 'U40'), ('plays', int), ('totalPlayTime', int)]
mostPlayedData = np.array(mostPlayedData, dtype=dtype) #convert to array
mostPlayedCount = np.sort(mostPlayedData, order='plays')[::-1]
mostPlayedTime = np.sort(mostPlayedData, order='totalPlayTime')[::-1]


# get top 5 artists

mostPlayedCount = mostPlayedCount[:5]
mostPlayedTime = mostPlayedTime[:5]

displaytable = PrettyTable()
displaytable.add_column("Artist", mostPlayedCount['artist'])
displaytable.add_column("Number of Plays", mostPlayedCount['plays'])
displaytable.add_column("Total Play Time", np.round(mostPlayedCount['totalPlayTime']/60000))
print('2024 Top Artists by Number of Plays')
print(displaytable)

displaytable = PrettyTable()
displaytable.add_column("Artist", mostPlayedTime['artist'])
displaytable.add_column("Number of Plays", mostPlayedTime['plays'])
displaytable.add_column("Total Play Time", np.round(mostPlayedTime['totalPlayTime']/60000))
print('2024 Top Artists by Play Time')
print(displaytable)