#!/usr/bin/python

import os
import re
import sys
import json
import hashlib
import unicodedata
from makeuplink import get_sentiment


# Load empty config constants.
MIDI_PATH = ''
LYRI_PATH = ''
API_KEY = ''


# Get constant config from a json config file.
# By default CONFIG.json

def get_config(CONFIG_FILE='CONFIG.json'):
    ''' Loads all the constants inside the  configuration file.
        By default CONFIG.json, but the get_config(newfile.json)
        takes as argument a file. The given file's contents should
        be in a JSON format. '''

    global LYRI_PATH, MIDI_PATH, API_KEY
    print '- Loading config file.'
    with open(CONFIG_FILE, 'r') as configfile:
        config = json.loads(configfile.read())
        MIDI_PATH = os.path.abspath(config["MIDI_PATH"]) + '/'
        LYRI_PATH = os.path.abspath(config["LYRI_PATH"]) + '/'
        API_KEY = config["MS_CS_API_KEY"]
    print 'MIDI PATH: ' + MIDI_PATH
    print 'LYRI PATH: ' + LYRI_PATH


# Remove any unwanted char from the file name.
def normalize(text):
    ''' This method does a regex search on the given text and removes
        any unwanted chars (ex: $*_;><) it also replaces any .txt file
        extension with .lyri and the .mid to .midi '''

    text = unicode(re.sub('[^\w\s.\s-]', '', text).strip().lower())
    text = unicode(re.sub('[-\s]+', '-', text))
    text = unicode(re.sub('.txt', '.lyri', text))
    text = unicode(re.sub('.mid', '.midi', text))
    print '--- NORMALIZED TO: ' + text
    return text


# Apply filename changes to a file.
def parse_file(filename, path):
    ''' This method renames a given file from a given path with a new
        normalized name. '''

    # Log event.
    print '-- PARSING FILE NAME: ' + filename

    newfilename = normalize(filename)
    print '--- RANAMING: '
    print path+filename
    print path+newfilename
    os.rename(path+filename, path+newfilename)


# Remove any white spaces or empty lines.
def parse_lyri(filename):
    ''' This method takes a text file (in our case .lyri) and removes any
        detected white spaces and empty lines. '''

    # Log event.
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
    ''' Create the Python dictionary and make a jsonstring out of it,
        then write all the data to a .json database. '''

    # Log event.
    print '-- INDEXING FILE: ' + filename

    # Initialize empty json object.
    jsonstring = {}

    # Assign a sentiment.
    sentiment = 'hpy' if score > 0.5 else 'sad'

    # Go trough the midi directory.
    midiname = 'null'
    for midi in os.listdir(MIDI_PATH):
        if str(midi)[:len(midi)-5] == filename[:len(filename)-5]:
            midiname = str(midi)

    # Add data to the json object as a dictionary.
    if midiname == 'null':
        print '--- No midi file found for ' + filename
    else:
        jsonstring.update({'score': score, 'filename': filename, 'sentiment': sentiment, 'midi': MIDI_PATH+midiname, 'hash': hash_contnet(filename)})

        # Log event.
        print '--- JSON: ', jsonstring

        # Write entry to the INDEX.json
        with open('INDEX.json', 'a') as mainindex:
            print '--- Wrote JSON to INDEX'
            mainindex.write(json.dumps(jsonstring))
            mainindex.write('\n')


def hash_contnet(filename):
    with open(LYRI_PATH+filename, 'r') as file:
        return hashlib.sha256(file.read()).hexdigest()


if __name__ == '__main__':
    # Load config file.
    get_config()

    # Check for extra arguments.
    if len(sys.argv) > 1:
        # Load lyri files locations.
        lyri_list = os.listdir(LYRI_PATH)

        # Parse midi file names.
        if 'midi' in sys.argv:
            # Load midi files locations.
            midi_list = os.listdir(MIDI_PATH)
            print '\n- START PARSING MIDI FILES'
            for midi in midi_list:
                parse_file(midi, MIDI_PATH)

        # Parse lyrics file names and content.
        if 'lyri' in sys.argv:
            print '\n- START PARSING LYRI FILES'
            for lyri in lyri_list:
                parse_file(lyri, LYRI_PATH)
                lyri_list = os.listdir(LYRI_PATH)
            for lyri in lyri_list:
                parse_lyri(lyri)

        # Write entries to .json and get sentiment from MS Text An. API
        if 'index' in sys.argv:
            print '\n- START INDEXING'
            lyri_list = os.listdir(LYRI_PATH)
            for lyri in lyri_list:
                # index_lyrics(lyri, get_sentiment(LYRI_PATH+lyri, API_KEY))

                # Debug only.
                index_lyrics(lyri, 0)
