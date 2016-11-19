import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer


nltk.download('punkt')

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')


def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0, 1]


print cosine_sim('a little bird', 'a little bird')
print cosine_sim('a little bird', 'a little bird chirps')
print cosine_sim('a little bird', 'a big dog barks')
print cosine_sim('', '')
