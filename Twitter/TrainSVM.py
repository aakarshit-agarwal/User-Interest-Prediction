import os
import numpy as np
import pandas
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.utils import shuffle


class labels:
    def __init__(self):
        self.d = {}

    def add(self, k, v):
        self.d[k] = v
        self.d[v] = k

    def remove(self, k):
        self.d.pop(self.d.pop(k))

    def get(self, k):
        return self.d[k]


labelIndex = labels()


def readJSON(path, file, count):
    name = file.split('.')
    temp = pandas.read_json(path + file)
    labelIndex.add(str(count), temp['label'][0])
    return temp


def trainSVM(dataSetFilePath, classifierFileName):
    JSONData = []
    count = 0
    for file in os.listdir(dataSetFilePath):
        JSONData.append(readJSON(dataSetFilePath, file, count))
        count += 1
    # print(JSONData)
    trainingText = []
    trainingLabel = []
    testingText = []
    testingLabel = []
    for each in JSONData:
        each = shuffle(each).reset_index(drop=True)
        trainingDataRange = [0, 299]
        testingDataRange = [300, len(each)]
        trainingText += each.ix[trainingDataRange[0]:trainingDataRange[1], 2].tolist()
        for index in each.ix[trainingDataRange[0]:trainingDataRange[1], 1].tolist():
            trainingLabel.append(labelIndex.get(index))
        testingText += each.ix[testingDataRange[0]:testingDataRange[1], 2].tolist()
        for index in each.ix[testingDataRange[0]:testingDataRange[1], 1].tolist():
            testingLabel.append(labelIndex.get(index))

    textClassifier = Pipeline([('vect', CountVectorizer()),
                               ('tfidf', TfidfTransformer()),
                               ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                                     alpha=1e-3, n_iter=5, random_state=42)),
                               ])

    textClassifier = textClassifier.fit(trainingText, trainingLabel)

    joblib.dump(textClassifier, classifierFileName)

    predicted = textClassifier.predict(testingText)
    accuracy = np.mean(predicted == testingLabel)
    print(accuracy)
    print(metrics.confusion_matrix(testingLabel, predicted))
    count = 0
    for i in range(len(testingLabel)):
        if testingLabel[i] != predicted[i]:
            count += 1
            print(testingText[i], labelIndex.get(testingLabel[i]), labelIndex.get(predicted[i]), sep=' | ')
    print(count)
    return accuracy