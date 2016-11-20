import os
import makeuplink


def index_lyrics(filename, score):
    with open('INDEX.db', 'a') as mainindex:
        mainindex.write(str(score) + ' ' + filename + '\n')


td = os.listdir('train_data')
for d in td:
    index_lyrics(d, 0)
