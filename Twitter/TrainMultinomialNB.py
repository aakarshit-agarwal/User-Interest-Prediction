import os
import numpy as np
import pandas
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
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

def trainNB(dataSetFilePath, classifierFileName):
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
        # print(each)
        each = shuffle(each).reset_index(drop=True)
        # print(each)
        trainingDataRange = [0, 599]
        testingDataRange = [600, len(each)]
        trainingText += each.ix[trainingDataRange[0]:trainingDataRange[1], 2].tolist()
        for index in each.ix[trainingDataRange[0]:trainingDataRange[1], 1].tolist():
            trainingLabel.append(labelIndex.get(index))
        testingText += each.ix[testingDataRange[0]:testingDataRange[1], 2].tolist()
        for index in each.ix[testingDataRange[0]:testingDataRange[1], 1].tolist():
            testingLabel.append(labelIndex.get(index))
    # print(trainingText)
    # print(trainingLabel)
    # print(testingText)
    # print(testingLabel)

    # countVect = CountVectorizer()
    # textTrainCounts = countVect.fit_transform(trainingText)
    # TfTransformer = TfidfTransformer()
    # textTrainTf = TfidfTransformer.fit_transform(textTrainCounts)
    # classifier = MultinomialNB().fit(textTrainTf, trainingLabel)

    textClassifier = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB())
    ])
    textClassifier = textClassifier.fit(trainingText, trainingLabel)

    joblib.dump(textClassifier, classifierFileName)

    predicted = textClassifier.predict(testingText)
    accuracy = np.mean(predicted == testingLabel)
    # print(accuracy)
    # print(metrics.confusion_matrix(testingLabel, predicted))
    count = 0
    for i in range(len(testingLabel)):
        if testingLabel[i] != predicted[i]:
            count += 1
            # print(testingText[i], labelIndex.get(testingLabel[i]), labelIndex.get(predicted[i]), sep=' | ')
    # print(count)
    return accuracy