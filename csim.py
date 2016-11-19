import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer

TRAINDATA = ['input2.txt']
USERINPUT = 'input1.txt'


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]


def get_related_words(word):
    return word


def read_file(filename):
    with open(filename, 'r') as source:
        return source.read()


def get_score(userKeys, databaseKeys):
    return cosine_sim(' '.join(userKeys), ' '.join(databaseKeys))


if __name__ == '__main__':
    nltk.download('punkt')

    stemmer = nltk.stem.porter.PorterStemmer()
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

    userinput = read_file(USERINPUT)
    words = []
    for word in userinput.split(' '):
        words.append(get_related_words(word))
    userinput = ' '.join(words)
    scores = []
    for filename in TRAINDATA:
        train_data_content = read_file(filename)
        words = []
        for word in train_data_content.split(' '):
            words.append(get_related_words(word))
        words = ' '.join(words)
        scores.append(get_score(words, userinput))

    print sorted(scores)
