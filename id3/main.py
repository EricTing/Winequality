#!/usr/bin/python
"""
Coding for data mining class at LSU, Dec. 2014

@author: Chenguang Zhang
"""

from id3tree import getDataFromFile, createID3Tree, classify

# loading data
print 'Reading records from file'
recordList = getDataFromFile('winequality-red-discrete.dat')
attributeNameList = recordList[0].keys()

# I. testing using whole dataset
# print 'Start constructing ID3 tree'
# tree = createID3Tree(recordList, attributeNameList, 'quality')
#
# #  write predictions into file, analyze using MATLAB afterwards
# predictionFile = open('prediction.dat', 'w')
# for record in recordList:
#     print>> predictionFile, classify(tree, record)
# predictionFile.close()


def adaBoostInterface(tree, featureValueList):
    """
    Use featureValueList instead of record for classification

    Warning: this function is HARDCODED, and must be modified for new problems!
    """
    attributeNameList = ["fixed acidity",
                         "volatile acidity",
                         "citric acid",
                         "residual sugar",
                         "chlorides",
                         "free sulfur dioxide",
                         "total sulfur dioxide",
                         "density",
                         "pH",
                         "sulphates",
                         "alcohol"]
    record = dict(zip(attributeNameList, featureValueList))
    return classify(tree, record)


def crossValidation(recordList, trainPercent=0.8, randomSeed=3):
    """
    Function for cross training and validation

    The default is train 80% to predict 20%, each time the recordList is
    splitted into trainingRecordList and validationRecordList.
    """
    from random import seed, shuffle
    seed(randomSeed)

    randomIndex = range(len(recordList))
    shuffle(randomIndex)

    trainingRecordList = [recordList[index] for index in
                          randomIndex[:int(trainPercent*len(recordList))]]
    validationRecordList = [recordList[index] for index in
                            randomIndex[int(trainPercent*len(recordList)):]]
    tree = createID3Tree(trainingRecordList, attributeNameList, 'quality')

    correct = incorrect = 0
    for record in validationRecordList:
        if classify(tree, record) == record['quality']:
            correct += 1
        else:
            incorrect += 1
    print 'correct: ', correct, 'incorrect: ', incorrect
    print 'accuracy: ', float(correct)/(correct + incorrect)

if __name__ == '__main__':
    for i in range(10):
        crossValidation(recordList, 0.8, i)
