from featureExtractor import *
from sampler import *
from sklearn.svm import SVC as SVM
from sklearn.linear_model import LogisticRegression as LR
from IO import *

"""
Function that classifies using an SVM approach on the input feature vectors
Xtrain and labels Ytrain. Validation sets Xval and Yval are used to tune 
hyper-parameters.
"""
def classifySVM(Xtrain, Ytrain, Xval, Yval):
    
    # set range of C parameters to test
    cvals = np.logspace(-2,7,40)

    # set range of gamma values to test
    gammas = np.logspace(-10,2,40)

    # find most accurate combination of C, gamma
    best_accuracy = 0
    best_model = None
    best_c = None
    best_g = None

    # cycle through all combinations of C, gamma
    for c in cvals:
        for g in gammas:
            clf = SVM(C=c, cache_size=200, class_weight=None, coef0=0.0, 
                    degree=3, gamma=g, kernel='rbf', max_iter=-1, 
                    probability=False, random_state=None, shrinking=True, 
                    tol=0.001, verbose=False)
            clf.fit(Xtrain, Ytrain)
            accuracy = clf.score(Xval, Yval)

            if accuracy >= best_accuracy:
                best_accuracy = accuracy
                best_model = clf
                best_c = c
                best_g = g

    print "Optimal SVM parameters: C = ", best_c, "and best gamma = ", best_g

    print "Best validation accuracy = " + str(best_accuracy)
    train_accuracy = best_model.score(Xtrain, Ytrain)
    print "With training accuracy = " + str(train_accuracy)

    return best_model

"""
Function that classifies using a logistic regression approach on the input 
feature vectors Xtrain and labels Ytrain. Validation sets Xval and Yval are 
used to tune hyper-parameters.
"""
def classifyLR(Xtrain, Ytrain, Xval, Yval):
    
    # set range of C parameters to test
    cvals = np.logspace(-2,7,40)

    # find most accurate value for C
    best_accuracy = 0
    best_model = None
    best_c = None

    # cycle through all values of C 
    for c in cvals:
        clf = LR(penalty='l2', dual=False, tol=0.0001, C=c, fit_intercept=True,
                intercept_scaling=1, class_weight=None, random_state=None) 
        clf.fit(Xtrain, Ytrain)
        accuracy = clf.score(Xval, Yval)

        if accuracy >= best_accuracy:
            best_accuracy = accuracy
            best_model = clf
            best_c = c

    print "Optimal LR parameters: C = ", best_c
    print "Best validation accuracy = " + str(best_accuracy)
    train_accuracy = best_model.score(Xtrain, Ytrain)
    print "With training accuracy = " + str(train_accuracy)

    return best_model

"""
Assigns point values to games based on prediction confidence, scores the picks
"""
def scoreSeason( predictionModel, confidenceModel, data ):

    # find predictions from preidction model
    ypred = predictionModel.predict(data.X)

    # find probabilities from confidence model
    yprob = confidenceModel.predict_proba(data.X)

    # associate probabilities with predictions
    yconf = []
    for i, yp in enumerate(ypred):
        yconf.append(yprob[i][yp])

    # assign point values by associated probability
    indexes = range(len(yconf))
    indexes.sort(key=yconf.__getitem__)

    # confidences
    confidences = np.zeros(len(yconf))
    conf = 1
    for index in indexes:
        confidences[index] = conf
        conf += 1

    return confidences

# run script
if __name__ == '__main__':
    
    # get feature vectors and results
    data = formFeatureVectors()

    # sample data into three data sets
    train, test, validate = sampleTrainTestValByYear(data)
    #straightSampleTrainTestVal(data)

    # find SVM model
    #svmModel = classifySVM(train.X, train.Y, validate.X, validate.Y)
    #print "Test accuracy = ", svmModel.score(test.X, test.Y), "\n"

    # find LR model
    lrModel = classifyLR(train.X, train.Y, validate.X, validate.Y)
    print "Test accuracy = ", lrModel.score(test.X, test.Y), "\n"
   
    scoringModel = lrModel
    predictionModel = lrModel

    # score a season
    confidences = scoreSeason( predictionModel, scoringModel, test )
    print_results( predictionModel, test, confidences )
    
    # print final predictions
    finalData = formFinalFeatureVectors()
    confidences = scoreSeason( predictionModel, scoringModel, finalData )
    print_predictions( predictionModel, finalData, confidences )
