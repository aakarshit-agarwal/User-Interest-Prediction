import json
import os

from sklearn.externals import joblib


def readJSON(path, name):
    """     Read a JSON File    """
    with open(path + name, encoding='utf8') as file:
        data = json.load(file)
        file.close()
    return data


def predict(filePath, classifierFile):
    labelsIndex = {
        0: 'economy',
        1: 'education',
        2: 'entertainment',
        3: 'food.',
        4: 'health',
        5: 'law',
        6: 'lifestyle',
        7: 'nature',
        8: 'politics',
        9: 'sports',
        10: 'technology'
    }
    query = []
    for file in os.listdir(filePath):
        fileData = readJSON(filePath, file)
        # print(fileData)
        for each in fileData:
            # print(each)
            query.append(each['text'])
    # print(query)
    textClassifier = joblib.load(classifierFile)
    predicted = textClassifier.predict(query)
    print(len(predicted))
    count = [0 for i in range(len(labelsIndex))]
    for i in range(len(predicted)):
        print(query[i], predicted[i], sep='\t|\t')
        count[int(predicted[i])] += 1
    for each in count:
        each /= len(predicted)

    return labelsIndex[count.index(max(count))]
