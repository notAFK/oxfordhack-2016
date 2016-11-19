import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import requests
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

TRAINDATA = ['input2.txt']
USERINPUT = 'input1.txt'
# THESAURUS_URL = 'http://www.thesaurus.com/browse/'
THESAURUS_URL = 'https://en.oxforddictionaries.com/thesaurus/'


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]


def get_related_words(word):
    # return word
    try:
        url = THESAURUS_URL + word
        print url
        headers = {'accept': 'text/html'}
        soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
        sense_groups = soup.find_all('section', 'sense_group_0')
        if len(sense_groups) == 0:
            return word

        divs = sense_groups[0].find_all('div', 'se2')[0].find_all('div', 'synGroup')
        words = []
        for div in divs:
            words.append(div.p.strong.string)
        return ' '.join(words)
    except Exception as ex:
        return word


def read_file(filename):
    with open(filename, 'r') as source:
        return source.read()


def get_score(userKeys, databaseKeys):
    return cosine_sim(userKeys, databaseKeys)


if __name__ == '__main__':
    nltk.download('punkt')

    stemmer = nltk.stem.porter.PorterStemmer()
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

    userinput = read_file(USERINPUT)
    words = []
    tokenizer = RegexpTokenizer(r"[\w']+")

    for word in set([w.lower() for w in tokenizer.tokenize(userinput) if w not in stopwords.words('english')]):
        words.append(get_related_words(word.lower()))
    userinput = ' '.join(words)
    scores = []
    for filename in TRAINDATA:
        train_data_content = read_file(filename)
        words = []
        for word in set([w.lower() for w in tokenizer.tokenize(train_data_content) if w not in stopwords.words('english')]):
            words.append(get_related_words(word.lower()))
        words = ' '.join(words)
        print words
        print userinput
        scores.append(get_score(words, userinput))

    print sorted(scores)
