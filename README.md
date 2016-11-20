# oxfordhack-2016
```python
from kitchen import coffee
```
### Documentation

#### Indexing
The ```indexer.py``` in conjuction with ```makeuplink.py``` create the ```INDEX.db``` which stores all the lyric names, artist and the sentiment score offered by [Microsoft Cognitive Services, Text Analytics API](https://www.microsoft.com/cognitive-services/en-us/text-analytics-api). The indexer script can be run in multiple ways: 
- ```python indexer.py pass``` which goes trough the training data directory and normalizes all filenames.
- ```python indexer.py lyrics``` which reads the content of each lyric file and removes any white/empty lines.
- ```python indexer.py server``` calls the indexer in production mode, meaning that it will read all training data then call the Microsoft API and index the lyrics filename with their appropiate score.

All indexed data respects the following format:

``` <score, ex: 0.345245> <filename, ex: artisit-name-song-name.txt> ```


#### Microsoft API
[Microsoft Cognitive Services, Text Analytics API](https://www.microsoft.com/cognitive-services/en-us/text-analytics-api) is used by sending text data (lyrics) to the Microsoft API then receiving a respons containing: keywords, language and sentiment.
