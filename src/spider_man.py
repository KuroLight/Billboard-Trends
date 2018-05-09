#! /usr/bin/env python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import requests
import os
import json
from bs4 import BeautifulSoup


token = os.environ.get('GENIUS_TOKEN')
# def get_token(file_path):
#     with open(file_path, 'r') as f:
#         token = f.read().replace('\n', '')
#         return token
# token = get_token('token.txt')
HEADERS = {'Authorization': 'Bearer %s' % (token)}

# edit here
<<<<<<< HEAD
START_YEAR = 1983  # inclusive
END_YEAR = 1990  # exclusive
=======
START_YEAR = 1952  # inclusive
END_YEAR = 1970  # exclusive
>>>>>>> 8056936a5e646210118e901f66e10e6db76e9a07


# https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/

def get_raw_content_from_url(url):
    """

    Args:
        url: string starts with 'http://'

    Returns: string of raw text of the html page

    """
    assert url.startswith('http://')
    response = requests.get(url=url)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response.text
    else:
        return 'get nothing from this html'


def get_lyrics_from_title_and_artist(i, title, artist):
    song_api_path = get_song_api_path_from_title_and_artist(i, title, artist)
    lyrics = get_lyrics_from_api_path(song_api_path)
    return i, title, artist, lyrics


def get_song_api_path_from_title_and_artist(i, title, artist):
    def pre_process_artist_name(artist):
        artist = artist.lower().replace("'s", "").replace("'", "").replace(
            " x ", " ")
        import string
        for punct in string.punctuation:
            artist = artist.replace(punct, ' ')
        return ' '.join(artist.split())

    def pre_process_title(title):
        return re.sub(r"""\(.*\)""", '', title)

    artist = pre_process_artist_name(artist)

    genius_search_url = 'http://api.genius.com/search'

    title = pre_process_title(title)
    query = {'q': title}

    # print('checking artist: %s, title: %s' % (artist, title))

    response = requests.get(genius_search_url, headers=HEADERS,
                            params=query).json()
    # print(response)
    for hit in response['response']['hits']:
        hit_artist_name = hit['result']['primary_artist']['name']
        hit_artist_name = pre_process_artist_name(hit_artist_name)
        # print('%s vs %s' % (hit_artist_name, artist))
        if hit_artist_name in artist or artist in hit_artist_name:
            song_api_path = hit['result']['api_path']
            print('#%s song: %s\tartist: %s' % (i + 1, title, artist))
            print(song_api_path)
            return song_api_path

    print('fail to get api path')
    return None


def get_lyrics_from_api_path(api_path):
    if not api_path:
        return None
    song_api_url = 'http://api.genius.com' + api_path
    response = requests.get(song_api_url, headers=HEADERS).json()
    song_real_url = 'http://genius.com' + response['response']['song']['path']

    song_content = get_raw_content_from_url(song_real_url)

    song_soup = BeautifulSoup(song_content, 'html.parser')
    [s.extract() for s in song_soup('script')]
    lyrics = song_soup.find('div', class_='lyrics').get_text()
    return lyrics.replace('\n', ' ')


class Song():

    def __init__(self, title, artist, lyrics):
        """
        simple song class to store basic info of a song
        Args:
            title: string, name of the song
            artist: string, name(s) of the singer
            lyrics: string, lyrics words seperated by spaces
        """
        self.song_info = {}
        self.song_info['title'] = title
        self.song_info['artist'] = artist
        self.song_info['lyrics'] = lyrics
        # self.title = title
        # self.artist = artist
        # self.lyrics = lyrics


class BillboardChart:

    def __init__(self, chart_name='hot-100', date=None):
        """
        simple billboard chart to store chart name and the specific date
        Args:
            chart_name: string, here we specify 'hot-100' for our purpose
            date: string, valid format is 'YYYY-MM-DD'
        """

        self.chart_name = chart_name

        if date and not re.match('\d{4}-\d{2}-\d{2}', str(date)):
            print('Wrong Date Format. Correct Format: YYYY-MM-DD')
            self.date = None
        else:
            self.date = date
        self.songs = []
        self.valid_lyrics_num = 0

    def load_chart_songs(self):

        if not self.date:
            url = 'http://www.billboard.com/charts/%s' % (self.chart_name)
        else:
            url = 'http://www.billboard.com/charts/%s/%s' % (
                self.chart_name, self.date)

        bb_page = get_raw_content_from_url(url)
        bb_soup = BeautifulSoup(bb_page, 'html.parser').find_all('article', {
            'class': 'chart-row'})

        title_and_artist = []
        for i, one_soup in enumerate(bb_soup):
            # if i > 2: break
            title_raw = one_soup.find('div', 'chart-row__title').contents
            try:
                title = title_raw[1].string.strip()
            except:
                print('get no title')
            try:
                if title_raw[3].find('a'):
                    artist = title_raw[3].a.string.strip()
                else:
                    artist = title_raw[3].string.strip()
            except:
                print('get no artist')

            print('#%s song: %s\tartist: %s' % (i + 1, title, artist))
            title_and_artist.append((i, title, artist))

        # https://morvanzhou.github.io/tutorials/data-manipulation/scraping/4-01-distributed-scraping/
        import multiprocessing as mp
        pool = mp.Pool(4)
        get_lyrics_jobs = [
            pool.apply_async(get_lyrics_from_title_and_artist,
                             args=(i, title, artist))
            for i, title, artist in title_and_artist
        ]
        songs = [j.get() for j in get_lyrics_jobs]
        for i, title, artist, lyrics in songs:
            if lyrics:
                self.valid_lyrics_num += 1
            song = Song(title, artist, lyrics)
            self.songs.append(song.song_info)

            # print('#%s song: %s\tartist: %s' % (i + 1, title, artist))


# def test():
#     genius_search_url = 'http://api.genius.com/search'
#     token = os.environ.get('GENIUS_TOKEN')
#     headers = {'Authorization': 'Bearer %s' % (token)}
#
#     query = {'q': 'Finesse'}
#     response = requests.get(genius_search_url, headers=headers,
#                             params=query).json()
#     print(response)


def get_all_saturdays_before_this_week(year):
    from datetime import date, timedelta
    d = date(year, 1, 1)
    d += timedelta(days=5 - d.weekday())
    if d.year < year:
        d += timedelta(days=7)
    while d.year == year:
        yield str(d)
        if d - date.today() > timedelta(days=0):
            return
        d += timedelta(days=7)


def get_one_week():
    if not os.path.exists('test'):
        os.mkdir('test')

    songs_in_year50 = []
    for year in range(2017, 2018):
        for i, week in enumerate(get_all_saturdays_before_this_week(year)):
            if i > 0:
                break
            if os.path.exists('test/billboard_hot100_%s.json' % (week)):
                continue

            print('\nweek - %s' % (week))
            songs_in_oneweek = BillboardChart(chart_name='hot-100', date=week)
            songs_in_oneweek.load_chart_songs()
            songs_in_year50.append(songs_in_oneweek)
            with open('test/billboard_hot100_%s.json' % (week), 'wt') as f:
                json.dump(songs_in_oneweek.songs, f, sort_keys=True, indent=4)

            valid_songs = songs_in_oneweek.valid_lyrics_num
            all_songs = len(songs_in_oneweek.songs)
            print('valid/all = %s/%s' % (valid_songs, all_songs))


def main():
    print('Getting billboard songs...')
    # chart_hot100_20180317 = BillboardChart(chart_name='hot-100', date='2018-03-15')
    # chart_hot100_20180317.load_chart_songs()
    # # for song in test.songs:
    # #     print('song: %s\nartist: %s\nlyrics:\n%s' % (song.title, song.artist, song.lyrics))
    #
    # print('valid lyrics num:', chart_hot100_20180317.valid_lyrics_num)

    songs_in_year50 = []
    for year in range(START_YEAR, END_YEAR):
        for week in get_all_saturdays_before_this_week(year):
            try:
                if not os.path.exists('lyrics'):
                    os.mkdir('lyrics')
                if os.path.exists('lyrics/billboard_hot100_%s.json' % (week)):
                    continue

                print('\nweek - %s' % (week))
                songs_in_oneweek = BillboardChart(chart_name='hot-100', date=week)
                songs_in_oneweek.load_chart_songs()
                songs_in_year50.append(songs_in_oneweek)
                with open('lyrics/billboard_hot100_%s.json' % (week), 'wt') as f:
                    json.dump(songs_in_oneweek.songs, f, sort_keys=True, indent=4)

                valid_songs = songs_in_oneweek.valid_lyrics_num
                all_songs = len(songs_in_oneweek.songs)
                print('valid/all = %s/%s' % (valid_songs, all_songs))
            except:
                pass
            
    # get_one_week()

    # valid_songs = sum([songs_in_oneweek.valid_lyrics_num for songs_in_oneweek in
    #                    songs_in_year50])
    # all_songs = sum(
    #     [len(songs_in_oneweek.songs) for songs_in_oneweek in songs_in_year50])
    # print('valid/all = %s/%s' % (valid_songs, all_songs))


if __name__ == '__main__':
    main()
