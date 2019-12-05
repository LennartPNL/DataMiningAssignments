# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 10:05:21 2018

@author: Lisa Tostrams

Simple decision boundary plotter for the MLPClassifier class in sklearn.neural_network. 
Example:
    
clf = sklearn.neural_network.MLPClassifier(...)
clf.fit(X,y)
plotter = MLPPlot.MLPPlot(X,y,clf)
plotter.plot_boundaries()

"""

import numpy as np
import matplotlib.pyplot as plt

class MLPPlot:
    def __init__(self, X,y,mlp):
        "Data X, label vector y, sklearn.neural_network.MLPClassifier object mlp"
        self.X = X
        self.y = y
        self.mlp = mlp
        
    def plot_boundaries(self):
        y_hat = self.mlp.predict(self.X)
        x0 = np.arange(min(self.X[:,0])-0.5, max(self.X[:,0])+0.5, 0.1)
        x1 = np.arange(min(self.X[:,1])-0.5, max(self.X[:,1])+0.5, 0.1)
        xx, yy = np.meshgrid(x0, x1, sparse=False)
        space = np.asarray([xx.flatten(),yy.flatten()]).T
        z = self.mlp.predict_proba(space)[:,1]
        plt.scatter(self.X[(y_hat==1),0],self.X[(y_hat==1),1],label='1')
        plt.scatter(self.X[(y_hat==0),0],self.X[(y_hat==0),1],label='0')
        h = plt.contourf(x0,x1,np.reshape(z,[len(x0),len(x0)]), levels=[0,0.5,1],colors=('orange','b'),alpha=0.1)
        plt.legend()
        plt.title('Decision boundary plot')
        plt.xlabel('$x_0$')
        plt.ylabel('$x_1$')
        plt.show()