# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
"""
Created on Mon Apr 14 09:01:18 2014

"""


def clusterPlot(X, clusterid, centroids=None, y=None):
    '''
    CLUSTERPLOT Plots a clustering of a data set as well as the true class
    labels. If data is more than 2-dimensional it should be first projected
    onto the first two principal components. Data objects are plotted as a dot
    with a circle around. The color of the dot indicates the true class,
    and the cicle indicates the cluster index. Optionally, the centroids are
    plotted as filled-star markers, and ellipsoids corresponding to covariance
    matrices (e.g. for gaussian mixture models).

    Usage:
    clusterplot(X, clusterid)
    clusterplot(X, clusterid, centroids=c_matrix, y=y_matrix)
    clusterplot(X, clusterid, centroids=c_matrix, y=y_matrix, covars=c_tensor)

    Input:
    X           N-by-M data matrix (N data objects with M attributes)
    clusterid   N-by-1 vector of cluster indices
    centroids   K-by-M matrix of cluster centroids (optional)
    y           N-by-1 vector of true class labels (optional)
    '''

    X = np.asarray(X)
    cls = np.asarray(clusterid)
    if y is None:
        y = np.zeros((X.shape[0], 1))
    else:
        y = np.asarray(y)
    if centroids is not None:
        centroids = np.asarray(centroids)
    K = np.size(np.unique(cls))
    C = np.size(np.unique(y))
    ncolors = np.max([C, K])

    # plot data points color-coded by class, cluster markers and centroids
    #plt.hold(True)
    colors = [0]*ncolors
    for color in range(ncolors):
        colors[color] = plt.cm.jet.__call__((color*255)//(ncolors-1))[:3]
    for i, cs in enumerate(np.unique(y)):
        plt.plot(X[(y == cs).ravel(), 0], X[(y == cs).ravel(), 1], 'o',
                 markeredgecolor='k', markerfacecolor=colors[i], markersize=6,
                 zorder=2)
    for i, cr in enumerate(np.unique(cls)):
        plt.plot(X[(cls == cr).ravel(), 0], X[(cls == cr).ravel(), 1], 'o',
                 markersize=12, markeredgecolor=colors[i],
                 markerfacecolor='None', markeredgewidth=3, zorder=1)
    if centroids is not None:
        for cd in range(centroids.shape[0]):
            plt.plot(centroids[cd, 0], centroids[cd, 1], '*', markersize=22,
                     markeredgecolor='k', markerfacecolor=colors[cd],
                     markeredgewidth=2, zorder=3)
    #plt.hold(False)

    # create legend
    legend_items = (np.unique(y).tolist() + np.unique(cls).tolist() +
                    np.unique(cls).tolist())
    for i in range(len(legend_items)):
        if i < C:
            legend_items[i] = 'Class: {0}'.format(legend_items[i])
        elif i < C + K:
            legend_items[i] = 'Cluster: {0}'.format(legend_items[i])
        else:
            legend_items[i] = 'Centroid: {0}'.format(legend_items[i])
    plt.legend(legend_items, numpoints=1, markerscale=.75, prop={'size': 9})
