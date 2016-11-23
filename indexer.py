#!/usr/bin/python
import os
import re
import sys
import json
import unicodedata
from makeuplink import get_sentiment

# Point to the path of the youtube scrapper.
# 'ok'      - folder for lyrics.
# 'midi'    - folder for midi files.
LYRI_PATH = 'youtubeScraper/ok2/'
MIDI_PATH = 'youtubeScraper/midi/'


# Remove any unwanted char from the file name.
def normalize(text):
    text = unicode(re.sub('[^\w\s.\s-]', '', text).strip().lower())
    text = unicode(re.sub('[-\s]+', '-', text))
    text = unicode(re.sub('.txt', '.lyri', text))
    print '--- NORMALIZED TO: ' + text
    return text


# Apply filename changes to a file.
def parse_file(filename, path):
    print '-- PARSING FILE NAME: ' + filename
    newfilename = normalize(filename)
    os.rename(path+filename, path+newfilename)


# Remove any white spaces or empty lines.
def parse_lyri(filename):
    print '-- PARSING LYRICS: ' + filename
    newlyrics = ''
    # Check each line.
    with open(filename, 'r') as sourcefile:
        for line in sourcefile:
            if line.strip():
                newlyrics += line
    # Write final version of lyri file.
    with open(filename, 'w') as sourcefile:
        sourcefile.write(newlyrics)


# Create entries in the INDEX.json database.
# Takes a lyrics file and a sentiment score.
def index_lyrics(filename, score):
    print '-- INDEXING FILE: ' + filename
    # Initialize empty json object.
    jsonstring = {}

    # Assign a sentiment.
    sentiment = 'hpy' if score > 0.5 else 'sad'

    # Go trough the midi directory.
    midiname = 'null'
    for midi in os.listdir(MIDI_PATH):
        if str(midi) == filename:
            midiname = str(midi)

    # Add data to the json object as a dictionary.
    if midiname == 'null':
        print '--- No midi file found for ' + filename
    else:
        print '--- JSON: ' + jsonstring
        jsonstring.update({'score': score, 'filename': filename, 'sentiment': sentiment, 'midi': MIDI_PATH+midiname})

        # Write entry to the INDEX.json
        with open('INDEX.json', 'a') as mainindex:
            print '--- Wrote JSON to INDEX'
            mainindex.write(json.dumps(jsonstring))
            mainindex.write('\n')


if __name__ == '__main__':
    # Load file names from main paths.
    lyri_list = os.listdir(LYRI_PATH)
    midi_list = os.listdir(MIDI_PATH)

    # Check for extra arguments.
    if len(sys.argv) > 1:
        # Parse midi file names.
        if 'midi' in sys.argv:
            print '\n- START PARSING MIDI FILES'
            for midi in midi_list:
                parse_file(midi, MIDI_PATH)
        # Parse lyrics file names and content.
        if 'lyri' in sys.argv:
            print '\n- START PARSING LYRI FILES'
            for lyri in lyri_list:
                parse_lyri(LYRI_PATH + lyri)
                parse_file(lyri, LYRI_PATH)
        # Write entries to .json and get sentiment from MS Text An. API
        if 'index' in sys.argv:
            print '\n- START INDEXING'
            for lyri in lyri_list:
                # index_lyrics(lyri, get_sentiment(LYRI_PATH+lyri))
                index_lyrics(lyri, 0)
