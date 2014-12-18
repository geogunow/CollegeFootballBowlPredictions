import random
from featureExtractor import dataSet
from pprint import pprint
from copy import deepcopy as copy

"""
Takes feature vectors Xdata with labels Ydata and forms 3 data sets:
train, test, and validate with proportions 60%, 20%, 20%
"""
def straightSampleTrainTestVal(data):

    # number of games in data set
    N = len(data.X)

    # round up counts for train and validate
    Ntrain = int(N*0.6) + 1
    Nval = int(N*0.8) + 1

    # initialize train, test, and validate sets
    train = dataSet()
    test = dataSet()
    validate = dataSet()

    # get variable sets
    trainVars = vars(train).values()
    testVars = vars(test).values()
    valVars = vars(validate).values()
    dataVars = vars(data).values()

    # cycle through all variables in the dataset
    for i, var in enumerate(dataVars):

        # copy appropriate variables
        trainVars[i] += var[:Ntrain]
        valVars[i] += var[Ntrain:Nval]
        testVars[i] += var[Nval:]

    return train, test, validate

"""
Takes feature vectors Xdata with labels Ydata and forms 3 data sets:
train, test, and validate with proportions 60%, 20%, 20%. Data is shuffled
randomly.
"""
#FIXME
def randomSampleTrainTestVal(data):

    # number of games in data set, sample initial indexes
    N = len(data.X)
    samples = random.sample(range(N),N)

    # round up counts for train and validate
    Ntrain = int(N*0.6) + 1
    Nval = int(N*0.8) + 1

    # initialize train, test, and validate sets
    train = dataSet()
    test = dataSet()
    validate = dataSet()

    # get variable sets
    trainVars = vars(train).values()
    testVars = vars(test).values()
    valVars = vars(validate).values()
    dataVars = vars(data).values()

    # cycle through all variables in the dataset
    for i, var in enumerate(dataVars):

        mangled_var = var[samples]

        # copy appropriate variables
        trainVars[i] += mangled_var[:Ntrain]
        valVars[i] += mangled_var[Ntrain:Nval]
        testVars[i] += mangled_var[Nval:]

    return train, test, validate
 
"""
Takes feature vectors Xdata with labels Ydata and forms 3 data sets:
train, validate, and test based on year (2003-2010, 2011-2012, 2013)
"""
def sampleTrainTestValByYear(data):

    # number of games in data set
    N = len(data.X)

    # initialize train, test, and validate sets
    train = dataSet()
    test = dataSet()
    validate = dataSet()

    # get variable sets
    trainVars = vars(train).values()
    testVars = vars(test).values()
    valVars = vars(validate).values()
    dataVars = vars(data).values()

    # cycle through all games
    for n in range(N):

        # check year for training
        if data.yearList[n] < 2012:

            # copy all variables from that game to training set
            for i, var in enumerate(dataVars):
                trainVars[i].append(var[n])

        # check year for test set (2013)
        elif data.yearList[n] == 2013:

            # copy all variables from that game to validation set
            for i, var in enumerate(dataVars):
                testVars[i].append(var[n])

        # remaining data  is validation set
        else:
            # copy all variables from that game to test set
            for i, var in enumerate(dataVars):
                valVars[i].append(var[n])

    return train, test, validate


