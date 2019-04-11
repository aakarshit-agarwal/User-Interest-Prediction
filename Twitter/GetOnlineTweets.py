import json
from pathlib import Path

import oauth2 as oauth
import unidecode

## Type your twitter keys here.
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)


def validateQuery(string):
    if ' ' in string:
        string.replace(' ', '+')
    if '@' in string:
        string.replace('@', '%40')
    elif '#' in string:
        string.replace('#', '%23')
    return string


def sendGetRequest(num, string):
    url = "https://api.twitter.com/1.1/search/tweets.json?q=" + string + "&lang=en&count=" + str(num)
    res, data = client.request(url)
    return res, data


def appendPreviousJSON(path, name):
    # if Path(path + name).is_file():
    #     with open(path + name, encoding='UTF-8') as file:
    #         data = json.load(file)
    #         file.close()
    #         pprint.pprint(data[-1:][0]['id'])
        # count = data[-1:][0]['id']
        # return data, count
    # else:
    return [], 0


def extractJSONData(data, tag, prevCount, allData):
    count = prevCount + 1
    data = json.loads(data)['statuses']
    for each in data:
        text = unidecode.unidecode(each['text'])
        allData.append({'id': count, 'text': text, 'label': tag})
        count += 1
    return count - 1, allData


def writeJSON(path, name, data):
    with open(path + name, 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=2)


def JSONToSet(data):
    temp = set()
    tag = ''
    for each in data:
        tag = each['label']
        temp.add(each['text'])
    return temp, tag


def setToJSON(data, tag):
    temp = []
    count = 1
    for each in data:
        temp.append({
            'id': count,
            'text': each,
            'label': tag
        })
        count += 1
    return temp


def getUserTweets(filePath, fileName, userName, label, count):
    userName = validateQuery(userName)
    response, APIData = sendGetRequest(count, userName)
    previousData, previousCount = appendPreviousJSON(filePath, fileName)
    lastCount, JSONData = extractJSONData(APIData, label.lower(), previousCount, previousData)
    setEntries, label = JSONToSet(JSONData)
    JSONData = setToJSON(setEntries, label)
    writeJSON(filePath, fileName, JSONData)
    return len(setEntries)
