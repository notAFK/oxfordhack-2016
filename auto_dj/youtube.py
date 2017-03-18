"""Get videos and lyrics from youtube.

You give a link for a playlist, and this script scraps everything,
getting the videos and the lyrics.
"""
from __future__ import unicode_literals
import re
import sys
import string
import hashlib
import youtube_dl
import requests
from lxml import html
from utils import *


def get_song_names(youtube_url):
    """Get the names of the song from an URL."""
    req = requests.session()
    page = req.post(youtube_url)
    tree = html.fromstring(page.content)
    return tree.xpath('//td[@class="pl-video-title"]/a/text()')


def get_instrumental_link(song_name):
    """Get the url for the instrumental of the song."""
    song_name = '+'.join(song_name.split(' '))
    payload = {'search_query': song_name}
    req = requests.session()
    page = req.post('https://www.youtube.com/results?', data=payload)
    tree = html.fromstring(page.content)
    instrumental_urls = tree.xpath('//div[@class="yt-lockup-content"]/h3/a/@href')
    if len(instrumental_urls) == 0:
        return ''
    return instrumental_urls[0]


def download_video(youtube_url, song_name):
    """Download the mp4 video."""
    song_name = ''.join(process_string(song_name))
    song_name = hashlib.sha256(song_name).hexdigest()
    ydl_opts = {
        'ignoreerrors': 'True',
        'outtmpl': MIDI_PATH + '/' + song_name + '.%(ext)s',
        'recodevideo': 'mp4'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])


def get_lyrics(song_name):
    """Get the lyrics for a song."""
    req = requests.session()
    song_name = '+'.join(song_name.split(' '))
    payload = {'k': song_name}
    lyrics_url = 'http://www.lyricsmania.com/searchnew.php?'
    page = req.post(lyrics_url, data=payload)
    tree = html.fromstring(page.content)
    lyrics_url = tree.xpath('//ul[@class="list-search"]/li/a/@href')
    page = req.post('http://www.lyricsmania.com' + lyrics_url[0])
    tree = html.fromstring(page.content)
    lyrics = tree.xpath('//div[@class="fb-quotable"]/text()')
    lyrics2 = tree.xpath(
        '//div[@class="fb-quotable"]/div[@class="p402_premium"]/text()')
    final_lyrics = ('\n'.join(lyrics) + '\n'.join(lyrics2)).replace('\t', '')
    final_lyrics = final_lyrics.replace("\n\n\n\n\n\n\n", '\n').encode('UTF-8')
    return final_lyrics


def write_lyrics(lyric, song_name):
    """Write the lyrics to file."""
    song_name = process_string(song_name)
    song_name = hashlib.sha256(song_name).hexdigest()
    with open(LYRICS_PATH + '/' + song_name + ".txt", "w") as file:
        file.write(lyric)


def process_string(name):
    """Remove non-ASCII symbols + useless information."""
    name = name.replace(' ', '').replace('.', '')
    printable = set(string.printable)
    name = ''.join(filter(lambda x: x in printable, name))
    regex = re.compile(r".*?\((.*?)\)")
    to_replace = re.findall(regex, name)
    name = name.replace('(' + ''.join(to_replace) + ')', '')
    return name.replace("\n", "")

def main():
    """Main function."""
    song_names = get_song_names(sys.argv[1])
    for song in song_names:
        write_lyrics(get_lyrics(song), song)
        youtube_url = get_instrumental_link(song + 'instrumental')
        if youtube_url == '':
            continue
        youtube_url = 'http://www.youtube.com' + youtube_url
        download_video(youtube_url, song)


if __name__ == '__main__':
    main()
