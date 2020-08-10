import requests
import re
import os
from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline

def make_soup(artist):
    """
    Request lyrics.com profile page of an artist and saves it into a BeautifulSoup object

    Parameters: artist = string
    Returns: soup = BeautifulSoup object
    """

    url = f'https://www.lyrics.com/artist/{artist}'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features='lxml')
    return soup

def create_song_list(soup):
    """
    Extract names and respective links of available songs
    Check for duplicates
    sort songs alphabetically
    Save list as file
    Return a list with all songs and their respective links

    Parameters: soup = BeautifulSoup object

    Returns:
    all_songs_and_links = list
    links = list
    """

    all_songs = []
    all_links = []
    all_songs_and_links = []
    html_songs = soup.body.find_all(attrs={'class':'tal qx'})
    for index in range(len(html_songs)):
        song = html_songs[index].text + ': '
        link = 'https://www.lyrics.com' + html_songs[index].find('a').get('href')
        song_and_link = song + link

        if (song in all_songs):
            continue
        elif ']' in song:
            continue
        else:
            all_songs.append(song)
            all_links.append(link)
            all_songs_and_links.append(song_and_link)
    all_songs_and_links.sort()
    try:
        os.mkdir(directory_path)
    except OSError as error:
        print('Folder already exists')
    file_name = f'{directory_path}/00_{artist}_all_songs.txt'
    with open (file_name, 'w') as file:
        for element in all_songs_and_links:
            file.write(element)
            file.write('\n')
    return all_links

def download_songs(all_links):
    """
    Takes a list of song links,
    creates a BeautifulSoup object to extract the lyrics
    downloads their lyrics,
    and saves each song's lyrics in a file with song as file name

    Parameters: all_links = list
    Returns: lyrics_of_all_songs = string
    """

    lyrics_of_all_songs = ''
    for link in all_links:
        url = link
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, features='lxml')
        if (soup.body.find(attrs={'class':'lyric-title'}) == None):
            continue
        song_name = soup.body.find(attrs={'class':'lyric-title'}).text
        song_name = song_name.replace(" ", "_")
        song_name = song_name.replace("/", "_")
        lyrics = soup.body.find(attrs={'id':'lyric-body-text'}).text
        directory_path = f'_RES/{artist}'
        file_name = f'{directory_path}/{artist}_{song_name}.txt'
        with open (file_name, 'w') as file:
                file.write(lyrics)
        text_corpus = lyrics_of_all_songs + lyrics + ' '
    return lyrics_of_all_songs

def save_all_lyrics_in_file(lyrics_of_all_songs):
    """
    Takes a string of all lyrics of the artist and saves them in a file

    Parameters: lyrics_of_all_songs = string
    Returns: nothing
    """

    directory_path = f'_RES/{artist}'
    file_name = f'{directory_path}/01_{artist}_all_lyrics.txt'
    with open (file_name, 'w') as file:
        file.write(lyrics_of_all_songs)

def train_your_model(text_corpus, labels):
    """
    Takes in all lyrics by chosen artists and respective artist names
    and transforms it into a model

    Parameters:
    text_corpus = list of strings
    labels = list of strings

    Returns:
    model
    """

    cv = CountVectorizer(stop_words='english')
    tf = TfidfTransformer()
    rf = RandomForestClassifier
    model = make_pipeline(cv, tf, rf)
    model.fit(text_corpus, labels)
    return model

def predict(model, new_text):
    new_text = [new_text]
    prediction = model.predict(new_text)

    return prediction[0]


LABELS = ['Foo-Fighters', 'Blink-182', 'Nine-Inch-Nails', 'Linkin-Park', 'Helge-Schneider']
TEXT_CORPUS = []

for artist in LABELS:
    directory_path = f'_RES/{artist}'
    file_name = f'{directory_path}/01_{artist}_all_lyrics.txt'
    if os.path.isfile(file_name):
        print (f"{artist} files already exist")
        with open (file_name, 'r') as file:
            lyrics = file.read().replace('\n', ' ')
    else:
        print (f"{artist} files do not exist, yet")
        soup = make_soup(artist)
        all_links = create_song_list(soup)
        lyrics = download_songs(all_links)
        save_all_lyrics_in_file(lyrics)
    TEXT_CORPUS.append(lyrics)

print(len(TEXT_CORPUS))
print(len(LABELS) == len(TEXT_CORPUS))

# MODEL = train_your_model(TEXT_CORPUS, LABELS)
# prediction = predict(MODEL, 'Texas')
# print(prediction)
