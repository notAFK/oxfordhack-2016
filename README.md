# oxfordhack-2016
```python
from kitchen import coffee
```
![winbadge](https://img.shields.io/badge/oxfordhack2016-winner-001faa.svg?style=flat-square)
![msbadge](https://img.shields.io/badge/microsoft-winner-333333.svg?style=flat-square)
### Documentation

#### Indexing
The ```indexer.py``` in conjuction with ```makeuplink.py``` create the ```INDEX.db``` which stores all the lyric names, artist and the sentiment score offered by [Microsoft Cognitive Services, Text Analytics API](https://www.microsoft.com/cognitive-services/en-us/text-analytics-api). The indexer script can be run in multiple ways: 
- ```python indexer.py pass``` which goes trough the training data directory and normalizes all filenames.
- ```python indexer.py lyrics``` which reads the content of each lyric file and removes any white/empty lines.
- ```python indexer.py server``` calls the indexer in production mode, meaning that it will read all training data then call the Microsoft API and index the lyrics filename with their appropiate score.

All indexed data is stored as JSON. 

#### Microsoft API
[Microsoft Cognitive Services, Text Analytics API](https://www.microsoft.com/cognitive-services/en-us/text-analytics-api) is used by sending text data (lyrics) to the Microsoft API then receiving a respons containing: keywords, language and sentiment.
