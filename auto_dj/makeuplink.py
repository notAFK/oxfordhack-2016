import json
import requests


def write_header(key):
    """Create standard header for Microsoft Text An. API."""
    header = {'Ocp-Apim-Subscription-Key': key,
              'Content-Type': 'application/json',
              'Accept': 'application/json'}
    return header


def write_doc_string(filelocation):
    """Prepare the document files for upload."""
    with open(filelocation, 'r') as inputfile:
        lyritext = inputfile.read()

    # Standard data format for MS Text An. API request.
    data = {
        "documents": [
            {
                "language": "en",
                "id": "1",
                "text": lyritext
            }
        ]
    }
    return json.dumps(data)


def get_sentiment(inputfile, apikey):
    """Get sentiment for a lyric."""
    print('GET SENTIMENT FOR: ' + inputfile)
    with requests.session() as shortname:
        answer = shortname.post(
            'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment',
            headers=write_header(apikey),
            data=write_doc_string(inputfile))
    returndict = json.loads(answer.content)
    print('RETURNED: ', returndict)
    return returndict['documents'][0]['score']
