# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 10:06:44 2018

@author: Pelle Michael Schwartz s147170, Jacob Frederiksen s163911
"""
import csv
import numpy as np
import matplotlib.pyplot as plt


# Load xls sheet with data

def dataLoad(filename):

    # Make inputdata contain a list of results using csv reader
    inputdata = []
    noerrors = True
    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile,delimiter=';')
        for row in csvReader:
            inputdata.append(row)
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
        elif data[i,10] < 0 :
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
        print("Data loaded.)
    return data



def histogram(line):
    plt.hist(data[:,line],bins='auto')
    
    
    
data = dataLoad("winequality-white.csv")
histogram(10)
