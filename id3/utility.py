"""
Coding for data mining class at LSU, Oct. 2014

@author: Chenguang Zhang
"""

def majorityValue(valueList):
    """ Find and return the majority value of a valueList """
    from collections import Counter
    c = Counter(valueList)
    return c.most_common()[0][0]


def isPure(valueList):
    """ Check if a list of value is pure, i.e., elements are identical """
    return valueList.count(valueList[0]) == len(valueList)

