import json
import requests


def write_header(key):
    # HEADER = '''
    # Ocp-Apim-Subscription-Key: ''' + key + '''
    # Content-Type: application/json
    # Accept: application/json
    # '''
    HEADER = {'Ocp-Apim-Subscription-Key': key,
              'Content-Type': 'application/json',
              'Accept': 'application/json'}
    return HEADER


def write_doc_string(filelocation):
    with open(filelocation, 'r') as inputfile:
        sometext = inputfile.read()

    DATA = {
     "documents": [
         {
             "language": "en",
             "id": "1",
             "text": sometext
             }]}
    return json.dumps(DATA)


def get_sentiment(inputfile):
    with requests.session() as shortname:
        answer = shortname.post('https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment', headers=write_header('82e0a934b6f44e0db5b33fc6635fd297'), data=write_doc_string(inputfile))
    returndict = json.loads(answer.content)
    print returndict
    return returndict['documents'][0]['score']
