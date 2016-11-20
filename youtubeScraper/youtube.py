from __future__ import unicode_literals
import youtube_dl
import requests
from lxml import html
import sys
import io


def getSongNames(youtubeLink):
    req = requests.session()
    page = req.post(youtubeLink)
    tree = html.fromstring(page.content)
    songNames = tree.xpath('//div[@class="yt-lockup-content"]/h3/a/text()')
    return songNames


def getInstrumLink(songNames):
    songNames = '+'.join(songNames.split(' '))
    payload = {
        'search_query': songNames
    }
    req = requests.session()
    page = req.post('https://www.youtube.com/results?', data=payload)
    tree = html.fromstring(page.content)
    instrumLink = tree.xpath('//div[@class="yt-lockup-content"]/h3/a/@href')
    return instrumLink[0]


def downloadYoutube(youtubeLink):
    ydl_opts = {
        'posprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3'
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtubeLink])


def getLyrics(songName):
    req = requests.session()
    songName = '+'.join(songName.split(' '))
    payload = {
        'k': songName
    }
    url = 'http://www.lyricsmania.com/searchnew.php?'
    page = req.post(url, data=payload)
    tree = html.fromstring(page.content)
    lyricLink = tree.xpath('//ul[@class="list-search"]/li/a/@href')

    url = 'http://www.lyricsmania.com' + lyricLink[0]
    page = req.post(url)
    tree = html.fromstring(page.content)
    lyrics = tree.xpath('//div[@class="fb-quotable"]/text()')
    lyrics2 = tree.xpath('//div[@class="fb-quotable"]/div[@class="p402_premium"]/text()')
    a = ('\n'.join(lyrics) + '\n'.join(lyrics2)).replace('\t', '')
    return a.replace("\n\n\n\n\n", '\n').encode('UTF-8')


def writeLyrics(lyric, songName):
    with io.FileIO(songName + ".txt", "w") as file:
            file.write(lyric)


def main():
    songNames = getSongNames(sys.argv[1])
    for song in songNames:
        writeLyrics(getLyrics(song), song)
        if (sys.argv[2] == 'yt'):
            youtubeLink = getInstrumLink(song + 'instrumental')
            youtubeLink = 'http://www.youtube.com' + youtubeLink
            downloadYoutube(youtubeLink)

if __name__ == '__main__':
    main()
