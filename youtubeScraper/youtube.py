from __future__ import unicode_literals
from subprocess import call
import youtube_dl
import requests
from lxml import html
import string
import re
import sys
import io

MIDI_PATH = './midi/'
LYRICS_PATH = './lyrics/'

def getSongNames(youtubeLink):
    req = requests.session()
    page = req.post(youtubeLink)
    tree = html.fromstring(page.content)
    songNames = tree.xpath('//td[@class="pl-video-title"]/a/text()')
    return songNames


def getInstrumLink(songNames):
    songNames = '+'.join(songNames.split(' '))
    payload = { 'search_query' : songNames }
    req = requests.session()
    page = req.post('https://www.youtube.com/results?', data = payload)
    tree = html.fromstring(page.content)
    instrumLink = tree.xpath('//div[@class="yt-lockup-content"]/h3/a/@href')
    return instrumLink[0]


def downloadYoutube(youtubeLink, songName):
    songName = ''.join(parseString(songName))
    ydl_opts = { 
            'ignoreerrors': 'True',
            'outtmpl': MIDI_PATH + songName + '.%(ext)s',
            'recodevideo': 'mp4'
            }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtubeLink])


def getLyrics(songName):
    req = requests.session()
    songName = '+'.join(songName.split(' '))
    payload = { 'k' : songName }
    lyricsUrl = 'http://www.lyricsmania.com/searchnew.php?'
    page = req.post(lyricsUrl, data = payload)
    tree = html.fromstring(page.content)
    lyricLink = tree.xpath('//ul[@class="list-search"]/li/a/@href')
    page = req.post('http://www.lyricsmania.com' + lyricLink[0])
    tree = html.fromstring(page.content)
    lyrics = tree.xpath('//div[@class="fb-quotable"]/text()')
    lyrics2 = tree.xpath('//div[@class="fb-quotable"]/div[@class="p402_premium"]/text()')
    finalLyric = ('\n'.join(lyrics) + '\n'.join(lyrics2)).replace('\t', '')
    finalLyric = finalLyric.replace("\n\n\n\n\n\n\n", '\n').encode('UTF-8')
    return finalLyric


def writeLyrics(lyric, songName):
    songName = ''.join(parseString(songName))
    with io.FileIO(LYRICS_PATH + songName + ".txt", "w") as file:
            file.write(lyric)


#remove non-ASCII symbols + useless information
def parseString(name):
    name = name.replace(' ', '').replace('.', '')
    printable = set(string.printable)
    name = ''.join(filter(lambda x: x in printable, name))
    regex = re.compile(".*?\((.*?)\)")
    toReplace = re.findall(regex, name)
    return name.replace('(' + ''.join(toReplace) + ')', '')
    

def main():
    songNames = getSongNames(sys.argv[1])
    for song in songNames:
        writeLyrics(getLyrics(song), song)
        youtubeLink = getInstrumLink(song + 'instrumental')
        youtubeLink = 'http://www.youtube.com' + youtubeLink
        downloadYoutube(youtubeLink, song)


if __name__ == '__main__':
    main()
