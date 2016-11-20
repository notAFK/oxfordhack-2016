import os
import sys
import json
import nltk
import string
import indexer
import requests
import makeuplink
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer


# Points to the directory that contains lyrics.
TRAIN_DATA_DIR = 'youtubeScraper/ok/'
# Points to the user input file.
USERINPUT = 'input1.txt'
# Path to main database index.
INDEXDB = 'INDEX.db'


def stem_tokens(tokens):
    ''' Return items that can stand alone or be combined. '''
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    ''' Remove untwanted char from the data stream. '''
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


def cosine_sim(text1, text2):
    ''' Return the cosine similarity, between two non zero vectors of an inner product space '''
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]


def get_related_words(word):
    ''' Deprecated method. '''
    return word


def read_file(filename):
    ''' Return the source of a file. '''
    with open(filename, 'r') as source:
        return source.read()


def get_score(userKeys, databaseKeys):
    ''' Calculate the score using the user defined terms and all the terms in the training database. '''
    return cosine_sim(userKeys, databaseKeys)


if __name__ == '__main__':
    # Make sure ntlk package is present.
    nltk.download('punkt')

    # Generate punctuation map.
    stemmer = nltk.stem.porter.PorterStemmer()
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

    # Normalize the stream.
    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

    # Read the user input file and prepare the variables.
    userinput = read_file(USERINPUT)
    words = []
    _GLOBALDICTIONARY = []
    tokenizer = RegexpTokenizer(r"[\w']+")

    # Start matching the words.
    for word in [w.lower() for w in tokenizer.tokenize(userinput) if w not in stopwords.words('english')]:
        words.append(get_related_words(word.lower()))
    userinput = ' '.join(words)
    scores = []
    # Check the training database files.
    for filename in os.listdir(TRAIN_DATA_DIR):
        train_data_content = read_file(TRAIN_DATA_DIR + '/' + filename)
        words = []
        for word in [w.lower() for w in tokenizer.tokenize(train_data_content) if w not in stopwords.words('english')]:
            words.append(get_related_words(word.lower()))
        words = ' '.join(words)
        try:
            # Calculate the score between two files.
            score = get_score(words, userinput)
            scores.append(score)
            # Update the dictionary with the filename and the score.
            _GLOBALDICTIONARY.append(dict({'score': score, 'filename': filename}))
        except:
            pass
#        print filename + ': ' + str(scores)
#    print sorted(scores)[-1]

    THISSENTIMENT = float(makeuplink.get_sentiment(USERINPUT))
    if THISSENTIMENT > 0.5:
        THISSENTIMENT = 'hpy'
    else:
        THISSENTIMENT = 'sad'

#    Print the global dictionary as a list.
#    for k, d in _GLOBALDICTIONARY.items():
#        print k, d

    sentimentdictlist = []
    with open(INDEXDB, 'r') as mainindex:
        for line in mainindex.readlines():
            jsondict = json.loads(line)
            if jsondict['sentiment'] == THISSENTIMENT:
                sentimentdictlist.append(jsondict)

    for gdict in _GLOBALDICTIONARY:
        for path in gdict['filename']:
            print path



    # finalscores = []
    # for mydict in sentimentdictlist:
    #     finalscores.append(mydict['score'])
    #
    # finalscores = sorted(finalscores)
    # highscore = finalscores[-1]
    # for mydict in sentimentdictlist:
    #     if mydict['score'] == highscore:
    #         print mydict
