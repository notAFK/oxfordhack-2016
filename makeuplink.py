import json
import requests


# Create standard header for Microsoft Text An. API
def write_header(key):
    HEADER = {'Ocp-Apim-Subscription-Key': key,
              'Content-Type': 'application/json',
              'Accept': 'application/json'}
    return HEADER


# Prepare the document files for upload.
def write_doc_string(filelocation):
    with open(filelocation, 'r') as inputfile:
        lyritext = inputfile.read()

    # Standard data format for MS Text An. API request.
    DATA = {
     "documents": [
         {
             "language": "en",
             "id": "1",
             "text": lyritext
             }]}
    return json.dumps(DATA)


def get_sentiment(inputfile):
    print 'GET SENTIMENT FOR: ' + inputfile
    with requests.session() as shortname:
        answer = shortname.post('https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment', headers=write_header('82e0a934b6f44e0db5b33fc6635fd297'), data=write_doc_string(inputfile))
    returndict = json.loads(answer.content)
    print 'RETURNED: ', returndict
    return returndict['documents'][0]['score']
