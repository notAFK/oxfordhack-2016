import json
import os
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
    DATA = {
     "documents": [
         {
             "language": "en",
             "id": "1",
             "text": filelocation
             }]}
    return json.dumps(DATA)


if __name__ == '__main__':
    # APIKEY = str(raw_input('API KEY: '))
    # write_header(APIKEY)
    with requests.session() as shortname:
        answer = shortname.post('https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment', headers=write_header('82e0a934b6f44e0db5b33fc6635fd297'), data=write_doc_string('input1.txt'))
    print answer.content
