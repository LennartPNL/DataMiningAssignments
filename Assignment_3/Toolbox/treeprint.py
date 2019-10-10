#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 10:02:37 2017

@author: ltostrams
"""


"""
NOTE: You don't have to change this code! (but you are allowed...)

A simple(?) tree visualizer for sklearn DecisionTreeClassifiers.

Based on suggestions from this thread: https://github.com/scikit-learn/scikit-learn/issues/6261
Adaptations by Lisa Tostrams, september 2017 for the course Data Mining in py27
Rewritten september 2018 for py36

Basic usage:
    dtc = sklearn.tree.DecisionTreeClassifier(...)
    dtc = dtc.fit(X,y)
    treeprint.tree_print(dtc, attributeNames, classNames)
    

"""
import operator

def tree_print(clf, attributeNames, classNames):
    """
    Print the tree of a sklearn DecisionTreeClassifier

    Parameters
    ----------
    clf : sklearn.tree.DecisionTreeClassifier object - A tree that has already been fit.
    attributeNames: vector of names of the variables
    classNames: vector of class names, names for the leafs
    """
    tlevel = _tree_rprint('', clf, attributeNames, classNames)
    print('<',end='')
    for i in range(5*tlevel - 2):
        print('-',end='')
    print('>')
    print('Tree Depth: ',tlevel)


def _tree_rprint(kword, clf, features, labels, node_index=0, tlevel_index=0, parent = 0, left=True):
    # Note: The DecisionTreeClassifier uses the Tree structure defined in:
    # 		github.com/scikit-learn/scikit-learn/blob/master/sklearn/tree/_tree.pyx
    #       it is an array based tree implementation.
    # indent the nodes according to their tree level
    # LT changes 2017: 
    #     draw tree from left to right
    #     added numbering
    #     added arrows
    # LT changes 2018:
    #     some cleaning
    #     
    #  TODO: 
    #        clean up ugly string formatting code
    #        the following should use the TREE_LEAF constant defined in _tree.pyx
    #        instead of -1, not quite sure how to get at it from the tree user level
    if clf.tree_.children_left[node_index] == -1:  # indicates leaf
        print(kword[:-4], end=' ' if kword else '')
        # get the majority label
        count_list = clf.tree_.value[node_index, 0]
        max_index, max_value = max(enumerate(count_list), key=operator.itemgetter(1))
        max_label = labels[max_index]
        print(max_label)
        return tlevel_index
    
    else:
        # compute and print node label
        feature = features[clf.tree_.feature[node_index]]
        threshold = clf.tree_.threshold[node_index]
        # recurse down the children
        left_index = clf.tree_.children_left[node_index]
        right_index = clf.tree_.children_right[node_index]
        #some formatting stuff
        string = kword[:-9]
        if(left_index<11):
            string = kword[:-8]   
        if(left and node_index is not 0):
            leftstr = string[:-1]
            leftstr = leftstr+' '
        else:
            leftstr = string
        tmp = leftstr
        for i in range(tlevel_index+1 - len(string)):
            leftstr = leftstr+' '
        #print left rule
        ltlevel_index = _tree_rprint(leftstr+'  |->{} then'.format(left_index), clf, features, labels, left_index, tlevel_index+1, parent=node_index)
        if(node_index is 0):
            print(' ', end='')
        print(tmp+'  |')
        print(kword, end=' ' if kword else '')
        #print current rule
        print('if {} =< {:4.2f}: go to {}, else go to {}'.format(feature, threshold, left_index, right_index))   
        #more formatting hell
        if(not left):
            rightstr = string[:-1]
            rightstr = rightstr+' '
        else:
            rightstr = string
        tmp = rightstr
        for i in range(tlevel_index+1 - len(string)):
            rightstr = rightstr+' '
        if(node_index is 0):
            print(' ', end='')
        print(tmp+'  |')
        #print right rule
        rtlevel_index = _tree_rprint(rightstr+'  |->{} else'.format(right_index), clf, features, labels, right_index, tlevel_index+1, parent=node_index, left=False)
        # return the maximum depth of either one of the children
        return max(ltlevel_index,rtlevel_index)
    
