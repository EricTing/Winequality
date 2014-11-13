#!/usr/bin/env python
"""grid search on SVC and decision tree 

search result print to file for plotting
"""

from sklearn import cross_validation
from sklearn import svm
from sklearn import tree

from sklearn.preprocessing import scale

from winequality_predict import loadDset, splitXandY, accuracy

def gridSearch4DecisionTree(X, y, max_sample = 20, test_size=0.33, random_state=0, ofn=''):
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, 
                                                                         y, 
                                                                         random_state=random_state,
                                                                         test_size=test_size)
    f = open(ofn, 'w')
    f.write("min_samples_split min_samples_leaf accuracy\n")
    paras = [(i,j) for i in range(1,max_sample) for j in range(1,max_sample)]
    for tup in paras:
        min_samples_split = tup[0]
        min_samples_leaf = tup[1]
        this_tree = tree.DecisionTreeClassifier(min_samples_leaf=min_samples_leaf,
                                             min_samples_split=min_samples_split)
        y_pred = this_tree.fit(X_train, y_train).predict(X_test)
        accu = accuracy(y_test, y_pred)
        f.write("%d %d %f\n" % (min_samples_split, min_samples_leaf, accu))

def gridSearch4Svc(X, y, test_size=0.33, random_state=0, ofn=''):
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, 
                                                                         y, 
                                                                         random_state=random_state,
                                                                         test_size=test_size)
    init_C = 0.00001;
    f = open(ofn, 'w')
    f.write("C Accuracy\n")
    for _ in range(12):
        y_pred = svm.SVC(C=init_C, random_state=random_state).fit(X_train, y_train).predict(X_test)
        accu = accuracy(y_test, y_pred)
        f.write("%f %0.2f" % (init_C, accu))
        init_C *= 10

def main():
    path = 'winequality-red.csv'
    # path = 'winequality-red.csv'
    dset = loadDset(path)

    X, y = splitXandY(dset)
    X = scale(X)

    print "--------------------------------------------------------------------------------"
    print "Grid search for SVC ..."
    ofn = 'svc_grid.txt'
    gridSearch4Svc(X, y, test_size=0.33, random_state=0, ofn=ofn)
    print "Grid search for SVC ... done"
    print "write the grid search result to %s" % (ofn)

    print "--------------------------------------------------------------------------------"
    print "Grid search for DecisionTreeClassifier ..."
    ofn = 'tree_grid.txt'
    gridSearch4DecisionTree(X, y, max_sample = 20, test_size=0.33, random_state=0, ofn=ofn)
    print "Grid search for DecisionTreeClassifier ... done"
    print "write the grid search result to %s" % (ofn)

if __name__ == '__main__':
    main()
