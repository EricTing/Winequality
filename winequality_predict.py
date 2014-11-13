#!/usr/bin/env python
"""play with the wine quality dataset using scikit-learn package
"""

import numpy as np
import pandas as pd

from sklearn import cross_validation
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import scale
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.lda import LDA
from sklearn import tree
from sklearn import svm

def loadDset(path):
    """load the original dataset
    Keyword Arguments:
    path -- input file path, csv format
    """
    return pd.read_csv(path, sep=';')


def splitXandY(dset):
    """get the attributes value matrix and target array
    Keyword Arguments:
    dset -- original dataset, pandas DataFrame
    """
    atr_cols = dset.columns[:-1]
    target_col = dset.columns[-1]
    X = dset[atr_cols].values
    y = dset[target_col].values

    return X, y

def cross_val_score(predictor, X, y, cv=5):
    scores = cross_validation.cross_val_score(
        predictor, X, y, cv=cv)

    return scores


def predict(predictor, X_train, y_train, X_test):
    pred_results = predictor.fit(X_train, y_train).predict(X_test)
    return pred_results


def accuracy(y_true,y_pred):
    return np.mean(y_true == y_pred)

def main():
    # red_path = 'winequality-red.csv'
    path = 'winequality-red.csv'
    dset = loadDset(path)
    dset = dset.reindex(np.random.permutation(dset.index))

    X, y = splitXandY(dset)
    X = scale(X)

    random_state = 0
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, 
                                                                         y, 
                                                                         random_state=random_state,
                                                                         test_size=0.33)

    mytree = MyTree()

    gnb = GaussianNB()
    lda = LDA()
    lgr = LogisticRegression(penalty='l1',random_state=random_state)
    svc = LinearSVC(random_state=random_state)
    d_tree = tree.DecisionTreeClassifier(random_state=random_state)
    svr = svm.SVC(random_state=random_state)

    pred_results = []
    for predictor in [gnb, lgr, lda, svc, d_tree, svr]:
        my_results = predictor.fit(X_train, y_train).predict(X_test)
        pred_results.append(my_results)
        print "--------------------------------------------------------------------------------"
        print predictor
        print "Accuracy: %0.2f" % accuracy(my_results, y_test)
        
    # to calculate the boost results
    votes_for_each = zip(*pred_results)  # unpack is needed

    def most_common(votes):     # to find consensus for each wine
        return max(set(votes), key=votes.count)
    
    consensus = [most_common(votes) for votes in votes_for_each]
    
    print "--------------------------------------------------------------------------------"
    accu = accuracy(y_test, consensus)
    print "Boost accuracy"
    print "Accuracy: %0.2f" % (accu)


if __name__ == '__main__':
    main()
