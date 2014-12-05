"""
Coding for data mining class at LSU, Nov. 2014

@author: Chenguang Zhang
"""

from heuristics import informationGain, getAttributeValueList
from utility import majorityValue, isPure


def selectSplitAttribute(recordList, targetAttributeName):
    """ Find the attribute to split record

        The attribute selected minimize entropy or equivalently,
        maximize the information gain.
    """
    attributeNameList = recordList[0].keys()
    splitAttributeName = None
    info_gain = 0
    for attributeName in attributeNameList:
        if attributeName != targetAttributeName:
            # evaluate the information gain obtained by using this attribute
            gain = informationGain(recordList, attributeName,
                                   targetAttributeName)
            if gain > info_gain:
                info_gain = gain
                splitAttributeName = attributeName
    # print 'Split attribute name: ', splitAttributeName
    return splitAttributeName


def getDataFromFile(fileName):
    """ Read data from a file and return a list of records

    Note: value of a record can be number or string, but in the case of string,
    it must NOT contain leading or trailing white spaces. So user should use
    tools like sed to remove them firstly before feeding to this program
    """

    import csv
    dataset = list(csv.reader(open(fileName, "r")))
    attributeNameList = dataset[0]

    recordList = []
    for record in dataset[1:]:
        recordList.append(dict(zip(attributeNameList, record)))
    print 'Available attributes for each record are: ', attributeNameList

    return recordList


def createID3Tree(recordList, attributeNameList, targetAttributeName):
    """ Construct a decision tree """
    recordList = recordList[:]
    targetValueList = getAttributeValueList(recordList, targetAttributeName)
    defaultTargetValue = majorityValue(targetValueList)

    if len(recordList) < 7 or len(attributeNameList) <= 0:
        # make leaf when dataset is small or no available attribute for spliting
        return defaultTargetValue

    elif isPure(targetValueList):
        # make leaf when dataset is pure
        return targetValueList[0]

    else:
        # split and construct the tree
        splitAttributeName = selectSplitAttribute(recordList,
                                                  targetAttributeName)
        if splitAttributeName is None:
            return defaultTargetValue  # !!!need review!!!
        tree = {splitAttributeName: {}}

        # generation defaultSplitValue: this is to handle the case when the
        # record lacks certain attribute or that attribute does not exist in the
        # tree
        splitValueList = getAttributeValueList(recordList, splitAttributeName)
        defaultSplitValue = majorityValue(splitValueList)

        # +next_line @ Nov. 10, each tree internal node now has an
        # 'defaultTargetValue' attribute
        tree[splitAttributeName]['defaultSplitValue'] = defaultSplitValue
        for value in set(getAttributeValueList(recordList, splitAttributeName)):
            subtree = createID3Tree(
                [record for record in recordList
                    if record[splitAttributeName] == value],
                [attributeName for attributeName in attributeNameList
                    if attributeName != splitAttributeName],
                targetAttributeName
            )
            tree[splitAttributeName][value] = subtree
    return tree


def classify(id3tree, record):
    if type(id3tree) != dict:
        return id3tree
    else:
        splitAttributeName = id3tree.keys()[0]  # get splitting attribute
        value = record[splitAttributeName]
        defaultValue = id3tree[splitAttributeName]['defaultSplitValue']

        if id3tree[splitAttributeName].has_key(value):
            return classify(id3tree[splitAttributeName][value], record)
        else:
            # print defaultValue, record[splitAttributeName]
            # print id3tree[splitAttributeName]
            return classify(id3tree[splitAttributeName][defaultValue], record)
