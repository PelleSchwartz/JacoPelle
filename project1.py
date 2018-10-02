# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 10:06:44 2018

@author: Pelle Michael Schwartz s147170, Jacob Frederiksen s163911
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as linalg
import matplotlib.pylab as pl
import pandas as pd
from sklearn import datasets

# Load xls sheet with data

def dataLoad(filename):

    # Make inputdata contain a list of results using csv reader
    inputdata = []
    noerrors = True
    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile,delimiter=';')
        for row in csvReader:
            inputdata.append(row)
    iris = pd.DataFrame(inputdata)
    print(iris.tail(1))
    inputdata.pop(0)
    data = np.asarray(inputdata).astype(np.float) #converting list to array containing all floats, no reason not to cast all to floats 
    
    removeline = False
    errorlines = []
    for i in range(0,len(data[:,0])):#Go through every line(N) of the data 
        if data[i,0] < 0: # fixed acidity
            print("Error in data line %s. fixed acidity: %s; Data line skipped"% (i+1,data[i,0]) )
            removeline = True #
        elif data[i,1] < 0:
            print("Error in data line %s. Volatile acidity %s; Data line skipped" % (i+1,data[i,1]) )
            removeline = True
        elif data[i,2] < 0 : # citric acid
            print("Error in data line %s. citric acid: %s; Data line skipped" % (i+1,data[i,2]) )
            removeline = True
        elif data[i,3] < 0 : # 
            print("Error in data line %s. residual sugar: %s; Data line skipped" % (i+1,data[i,3]) )
            removeline = True
        elif data[i,4] < 0 :
            print("Error in data line %s. chloride: %s; Data line skipped" % (i+1,data[i,4]) )
            removeline = True
        elif data[i,5] < 0 : 
            print("Error in data line %s. free sulfur: %s; Data line skipped" % (i+1,data[i,5]) )
            removeline = True
        elif data[i,6] < 0 :
            print("Error in data line %s. total sulfur: %s; Data line skipped" % (i+1,data[i,6]) )
            removeline = True
        elif 0 > data[i,7] > 1.5 :
            print("Error in data line %s. density: %s; Data line skipped" % (i+1,data[i,7]) )
            removeline = True
        elif 0 > data[i,8] > 14 :
            print("Error in data line %s. pH: %s; Data line skipped" % (i+1,data[i,8]) )
            removeline = True
        elif data[i,9] < 0 :
            print("Error in data line %s. sulpates: %s; Data line skipped" % (i+1,data[i,9]) )
            removeline = True
        elif 0 > data[i,10] > 30 :
            print("Error in data line %s. alchohol: %s; Data line skipped" % (i+1,data[i,10]) )
            removeline = True
        elif 10 < data[i,11] < 0 or not data[i,11].is_integer():
            print("Error in data line %s. quality: %s; Data line skipped" % (i+1,data[i,11]) )
            removeline = True
    
        if removeline == True:
            errorlines.append(i) #store lines in a list to remove after going through the data set
            removeline = False
            noerrors = False
    data = np.delete(data,errorlines,axis = 0) # remove found error lines from data
    if noerrors:
        print("Data loaded. No errors found.")
    else:
        print("Data loaded.")
    return data

def histogram(line,title,xlab):
    plt.hist(data[:,line],bins='auto')
    plt.title(title)
    plt.ylabel('Amount')
    plt.xlabel(xlab)
#    plt.savefig(title +'.png')
#    plt.show()
    
def scatter(x,y,xlab,ylab,title):
    plt.plot(data[:,x],data[:,y],'bo',linewidth = 0)    
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)
#    plt.savefig(title +'.png')
#    plt.show()
    

   
data = dataLoad("winequality-white.csv")

plt.figure(figsize=(10, 6),dpi=100)
plt.subplot(1,2,1)
histogram(11,"Quality","Score")
plt.subplot(1,2,2)
histogram(10,"Alcohol %","Alcohol %")
plt.show()

scatter(10,11,'Alcohol %','Quality','Quality compared to alcohol')

datatrimmed = data[:,0:12] # trim out ratings to group these


n = range(3,10)
y = data[:,11] #column with ratings
N,M = datatrimmed.shape

Xc = datatrimmed - np.ones((N,1))*datatrimmed.mean(0)

## Following is from ex2_2_2.py provided by the course
# PCA by computing SVD of Y
U,S,V = linalg.svd(Xc,full_matrices=False)
#U = mat(U)
V = V.T

# Compute variance explained by principal components
rho = (S*S) / (S*S).sum() 

# Project data onto principal component space
Z = Xc @ V

# Plot variance explained
plt.figure(figsize=(10, 6),dpi=100)
plt.subplot(1,2,1)
plt.plot(range(1,M+1),rho,'o-')
plt.title('Variance explained by principal components');
plt.xlabel('Principal component');
plt.ylabel('Variance explained value');
plt.grid()

covar = np.cov(data.T)

plt.subplot(1,2,2)

plt.title('Wine attributes projected on the first PC')
for c in n:
    # select indices belonging to class c:
    class_mask = (y == c)
    plt.plot(Z[class_mask,0], data[class_mask,11], 'o', fillstyle='none')
plt.legend(n)
plt.grid()

plt.xlabel("PC1")
plt.ylabel("Quality")

summary = np.ones((5,M))
for i in range(0,M):
    summary[0,i] = np.percentile(data[:,i],75)
    summary[1,i] = np.mean(data[:,i])
    summary[2,i] = np.percentile(data[:,i],25)
    summary[3,i] = np.std(data[:,i])
    summary[4,i] = np.var(data[:,i])
summary = np.round(summary, 5)


## Components needed for to explain more than 90% of the variance.
rhosum = 0
for i in range(len(rho)):
    rhosum += rho[i]
    if rhosum > 0.9:
        break
print(i+1,"PCA component(s) needed for +90 percent")



    
