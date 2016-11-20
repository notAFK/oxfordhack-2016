import os
import re
import sys
import json
import unicodedata
from makeuplink import get_sentiment

DATAPATH = 'youtubeScraper/ok/'
MIDIPATH = 'youtubeScraper/midi/'


def normalize(value):
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))
    return value


def passfile(filename):
    newfilename = normalize(filename)
    os.rename(DATAPATH+filename, DATAPATH+newfilename)


def passmidi(filename):
    newfilename = normalize(filename)
    os.rename(MIDIPATH+filename, MIDIPATH+newfilename)


def passlyrics(filename):
    NEWFILE = ''
    with open(filename, 'r') as sourcefile:
        for line in sourcefile:
            if line.strip():
                NEWFILE += line
                print line
                print 'STRIPE!'
    with open(filename, 'w') as sourcefile:
        sourcefile.write(NEWFILE)


def index_lyrics(filename, score):
    jsonstring = {}
    sentiment = ''
    if score > 0.5:
        sentiment = 'hpy'
    else:
        sentiment = 'sad'
    midiname = ''
    for midi in os.listdir(MIDIPATH):
        if str(midi).startswith(filename[0:8]):
            midiname = str(midi)
    jsonstring.update({'score': score, 'filename': filename, 'sentiment': sentiment, 'midi': MIDIPATH+midiname})

    with open('INDEX.db', 'a') as mainindex:
        mainindex.write(json.dumps(jsonstring))
        mainindex.write('\n')

if __name__ == '__main__':
    td = os.listdir(DATAPATH)
    if len(sys.argv) > 1:
        if sys.argv[1] == 'midi':
            for d in os.listdir(MIDIPATH):
                passmidi(d)
    for d in td:
        if len(sys.argv) > 1:
            if sys.argv[1] == 'pass':
                passfile(d)
            elif sys.argv[1] == 'lyrics':
                passlyrics(DATAPATH+d)
        else:
            index_lyrics(d, get_sentiment(DATAPATH+d))
