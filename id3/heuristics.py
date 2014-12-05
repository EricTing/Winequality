"""
Coding for data mining class at LSU, Oct. 2014

@author: Chenguang Zhang
"""

from collections import defaultdict
def entropy(valueList):
    """Calculate and return entropy

    Given a list of values of identical type (the type can be int, string, etc.)
    calcuate the information entropy of this list by \sum(-p*log(2,p))
    """
    from math import log
    # use defaultdict for counting
    nvalue = len(valueList)

    counter = defaultdict(int)
    for v in valueList:
        counter[v] += 1
    # print 'Number of categories: %d'%(len(counter.keys()))

    entropy = 0
    for item in counter.items():
        p = float(item[1])/nvalue
        entropy += (-p*log(p,2))

    return entropy


def getAttributeValueList(recordList, attributeName):
    """ Given a list of record, create a new valueList of an attribute."""
    return [record[attributeName] for record in recordList] # return valueList


def informationGain(recordList, attributeName, targetAttributeName):
    """ Calculate the gain of information by spliting the records

    The information gain is entropy(splitted records) - entropy(whole records)
    note that entropy of the splitted records is the sum of entropy of each
    subset, weighted by its proportion
    """
    entropyBeforeSplit = entropy(getAttributeValueList(recordList, targetAttributeName))
    entropyAfterSplit = 0

    subsetDict = defaultdict(int)
    for record in recordList:
        subsetDict[record[attributeName]] += 1
    # number of subsets by splitting is len(recordSubset.keys())

    for subsetValueKey, subsetItemCount in subsetDict.iteritems():
        weight = 1.0*subsetItemCount/len(recordList)
        recordSubset = [record for record in recordList if record[attributeName] == subsetValueKey]
        entropyAfterSplit += weight * entropy(getAttributeValueList(recordSubset, targetAttributeName))

    return entropyBeforeSplit - entropyAfterSplit
