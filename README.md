# AutoDJ - Oxford Hack 2016
```python
from kitchen import coffee
```
![winbadge](https://img.shields.io/badge/oxfordhack2016-winner-FFB900.svg?style=flat-square)
![msbadge](https://img.shields.io/badge/microsoft-winner-64C200.svg?style=flat-square)
![license](https://img.shields.io/badge/license-!AFK-00A1F3.svg?style=flat-square)
![neuraln](https://img.shields.io/badge/neuralnetworks-yes-FF2E00.svg?style=flat-square)

---
Description
===

### Inspiration
Lots of people are creative enough to write awesome lyrics, but they lack the musical knowledge to create songs with them. What if we had a program to generate a good song depending on the text input? That's exactly what **AutoDJ** does.


### What it does
Using [**Microsoft's Text Analysis API from Cognitive Services**](https://www.microsoft.com/cognitive-services "Microsoft's Cognitive Services API"), we analyse the key-phrases of the input text given by the user. We also look if it is happy / sad, using the **sentiment analysis** feature of the API. We compare the resulted features against a large collection of song lyrics, using the cosine similarity measure. The first few best matches are then fed into a **Restricted Boltzmann Machine** that generates a new song from them.


### How we built it
First we downloaded a large number of popular songs from YouTube (the instrumentals only) and their lyrics separately from different websites, we parse the midi and lyrics files then index them in a ```JSON``` database. After that we have a script that calls the **Microsoft's Text Analysis API** and gets the **key phrases** for the user input, and compares it using the **cosine similarity** measure with the key phrases from all the lyrics indexed. We take the instrumental songs of the best matches (encoded as ```.midi```) and feed them into the neural network that generates a new ```.midi``` with similar sounding.

### Challenges we ran into
It's very hard to generate new music, as this is a cutting-edge current research topic. It is also very hard (and thus unreliable) to convert ```.mp3``` into ```.midi```. We had some troubles doing that, and even now it's not too accurate. Of course we also had the usual issues with permissions, dependencies, ƲƮƑ-8, etc., but who doesn't have those ?

---
Documentation
===

### ```CONFIG.json```
```json
{
  "MIDI_PATH": "PATH/TO/ALL/THE/MIDI/FILES/",
  "LYRI_PATH": "PATH/TO/ALL/THE/LYRI/FILES",
  "MS_CS_API_KEY": "<INSERT KEY HERE>",
  "INPUT_FILE": "USERINPUTFILE.txt"
}
```
By default the ```MIDI_PATH``` is inside ```data/midi/``` and the ```LYRI_PATH``` is ```data/lyri/```.

The ```MS_CS_API_KEY``` is the 32 character long string containing both letters and numbers provided by the Microsoft API.
This key can be found on [My Account](https://www.microsoft.com/cognitive-services/en-US/subscriptions) page and should look something like this:
![myaccapikey](http://i.imgur.com/ijI54d0.png)

The default input file for the user input (transferred using PHP from the main website) is stored in ```input1.txt```.

### ```youtubeScrapper```
Praesent tincidunt accumsan orci vel eleifend. Vestibulum et luctus purus. Vestibulum eu rhoncus enim. Donec pretium posuere scelerisque. Nam nec tellus orci. Ut ac magna tempor, tincidunt nulla eu, pretium elit. Vestibulum faucibus neque sed neque rutrum, a dignissim diam finibus. Vivamus quis consectetur neque.

### ```indexlink```
The ```indexer.py``` in conjuction with ```makeuplink.py``` create the ```INDEX.json``` which stores all the lyric names, artist and the sentiment score offered by [Microsoft Cognitive Services, Text Analytics API](https://www.microsoft.com/cognitive-services/en-us/text-analytics-api). The indexer script can be run with multiple arguments: 
- ```python indexer.py midi``` which goes trough the specified ```MIDI_PATH``` and normalizes all file names.
- ```python indexer.py lyri``` which goes trough the specified ```LYRI_PATH``` and normalizes all file names, after that it removes any white spaces and empty lines from inside the lyrics file.
- ```python indexer.py index``` calls the indexer in production mode, meaning that it will read all training data then call the Microsoft API and index: the lyrics ```filename``` with their appropiate sentiment ```score``` and the coresponding ```midi``` file.
All indexed data is stored in ```JSON``` format, representing ```Python Dictionary``` objects.

### ```csim```
Pellentesque viverra nunc vel nisi viverra porta. Aliquam dolor quam, sodales et arcu eget, posuere hendrerit magna. Vestibulum non rhoncus est. Pellentesque ullamcorper nibh a mi finibus volutpat. Donec facilisis quam massa, eget tincidunt tortor pretium vel. Aliquam erat volutpat. Mauris elementum turpis ut dui venenatis, eget porttitor eros faucibus. 

### ```rbm``` - Restricted Boltzmann Machine
In ligula massa, dignissim a sapien vitae, ornare dignissim leo. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Curabitur nec lectus libero. Sed metus sapien, interdum non porttitor in, mattis et nisl. Praesent nec tincidunt nisi. Vivamus volutpat urna id rhoncus eleifend. Mauris ligula urna, sollicitudin quis erat in, pulvinar blandit tellus. Donec felis nibh, sagittis nec feugiat at, gravida id mauris. Phasellus sed odio at urna bibendum hendrerit nec nec augue. Donec sit amet sodales lectus. Quisque posuere sapien vitae ex aliquam tincidunt. Maecenas ut odio sit amet sapien dapibus gravida et eu felis. 

References
===
### Microsoft API
[Microsoft Cognitive Services, Text Analytics API](https://www.microsoft.com/cognitive-services/en-us/text-analytics-api) is used by sending text data (lyrics) to the Microsoft API then receiving a respons containing: keywords (obtained using  Natural Language Processing Natural Language Processing), language and sentiment score (represented by a numeric score between 0 and 1). Scores close to 1 indicate positive sentiment and scores close to 0 indicate negative sentiment. Sentiment score is generated using classification techniques. 

### Devpost Submission - [Devpost Link](https://devpost.com/software/autodj-i87zrp "https://devpost.com/software/autodj")
The Devpost Page was created for the Oxford Hack 2016, 24 hackathon.
### License - !AFK
The **!AFK** License is a derivative of [Simple Machine License](http://www.simplemachines.org/about/smf/license.php)
### Video - [Video Link](https://www.youtube.com/watch?v=qlJH8-5ZJlk)
The video on YouTube, contains a demonstration and explanation (5 minutes long) of how the program works.
