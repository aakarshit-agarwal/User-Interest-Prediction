import json
import os
import re

# Regular expressions for text cleanup
linkRE = re.compile(r'http[^\s|"]*', re.IGNORECASE)
# reTweetRE = re.compile(r'\bRT @[^\s]*', re.IGNORECASE)
reTweetRE = re.compile(r'\bRT @', re.IGNORECASE)
atSignRE = re.compile(r'[\w]*@[^\s]*')
ampRE = re.compile(r'&amp;')
newLineRE = re.compile(r'\n')
hashTagRE = re.compile(r'([A-Z]+[^A-Z|^\s]*)')
# hashTagRE = re.compile(r'#(\w*)')
symbolsRE = re.compile(r'[^a-z|^A-Z]')
shortWordsRE = re.compile(r'\W*\b\w{1}\b')
multipleWhiteSpaceRE = re.compile(r'[\s]{2,}')


def readJSON(path, name):
    """     Read a JSON File    """
    with open(path + name, encoding='utf8') as file:
        data = json.load(file)
        file.close()
    return data


def writeJSON(path, name, data):
    """     Write a JSON File    """
    with open(path + name, 'w') as file:
        json.dump(data, file, indent=2)


def hashTag(string):
    reg = re.compile(r'#([A-Z]*[a-z]*)(\w*)')
    string = re.sub(reg, lambda x: x.group(1) if not x.group(2) else x.group(1) + ' ' + hashTag('#' + x.group(2)),
                    string)
    print(string)
    return string


def normalizeTweets(data, options):
    """     Normalize Tweets     """
    for each in data:
        tweet = each['text']
        if 'links' in options:
            tweet = re.sub(linkRE, ' ', tweet)
        if 'retweet' in options:
            tweet = re.sub(reTweetRE, ' ', tweet)
        # tweet = re.sub(atSignRE, ' ', tweet)
        tweet = re.sub(ampRE, ' ', tweet)
        tweet = re.sub(newLineRE, ' ', tweet)
        if 'hashtag' in options:
            tweet = re.sub(hashTagRE, r'\1 ', tweet)
        # tweet = re.sub(hashTagRE, lambda x: hashTag(x.group()), tweet)
        if 'symbols' in options:
            tweet = re.sub(symbolsRE, ' ', tweet)
        tweet = re.sub(shortWordsRE, ' ', tweet)
        tweet = re.sub(multipleWhiteSpaceRE, ' ', tweet)
        if 'lowercase' in options:
            tweet = tweet.lower()
        each['text'] = tweet.strip()
    return data


def normalizeJSONData(rawFilePath, finalFilePath, options):
    print("List", os.listdir(finalFilePath))
    for file in os.listdir(finalFilePath):
        os.remove(finalFilePath + file)
    print("List2", os.listdir(rawFilePath))
    for file in os.listdir(rawFilePath):
        trainingData = readJSON(rawFilePath, file)
        trainingData = normalizeTweets(trainingData, options)
        writeJSON(finalFilePath, file, trainingData)
