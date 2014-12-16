"""
Prints all bowl games
"""
def print_games():
    games = set()
    bowlGames = '../Data/bowlGames.csv'
    with open('../bowl_list','w') as fw:
        with open(bowlGames,'r') as fr:
            lines = fr.readlines()
            for line in lines[1:]:
                fields = line.split(',')
                bowl = fields[7]
                if bowl not in games:
                    games.add(bowl)
                    print str(bowl)
                    fw.write(bowl + '\n')

"""
Function that takes a model and a data set and prints the predictions as well
as actual results
"""
def print_results(model, data, confidences = None):
    
    # make predictions using model
    Ypredict = model.predict(data.X)

    # tally correct and incorrect results
    talIncorrect = 0
    talCorrect = 0
    score = 0
    
    # cycle through all points in the data set
    for i, yp in enumerate(Ypredict):
        
        print data.nameList[i], ' ', data.yearList[i], ': ', data.teamAList[i], \
                ' vs ', data.teamBList[i]
        

        # determine confidence
        conf = 1
        if confidences is not None:
            conf = int(confidences[i])

        # display prediciton
        if yp == 1:
            print "Prediction: ", data.teamAList[i], " over ", \
                    data.teamBList[i], "(", conf, ")"
        else:
            print "Prediction: ", data.teamBList[i], " over ", \
                    data.teamAList[i], "(", conf, ")"

        # determine success
        success = 'N'
        if data.Y[i] == yp:
            success = 'Y'

        # display result
        if data.Y[i] == 1:
            print "Result: ", data.teamAList[i], " over ", \
                    data.teamBList[i], "(", success, ") \n"
        else:
            print "Result: ", data.teamBList[i], " over ", \
                    data.teamAList[i], "(", success, ") \n"

        # tally performance
        if data.Y[i] == yp:
            talCorrect += 1
            score += conf
        else:
            talIncorrect += 1

    # print overall performance
    acc = float(talCorrect) / (talCorrect + talIncorrect)
    print "Summary: ", talCorrect, " correct and ", talIncorrect,\
            " incorrect -> ", acc, "% accuracy"
    print "Score = ", score


"""
Function that takes a model and a data set and prints just predictions with
confidence points
"""
def print_predictions(model, data, confidences = None):
    
    # make predictions using model
    Ypredict = model.predict(data.X)

    # cycle through all points in the data set
    for i, yp in enumerate(Ypredict):
        
        print data.nameList[i], ' ', data.yearList[i], ': ', data.teamAList[i], \
                ' vs ', data.teamBList[i]
        

        # determine confidence
        conf = 1
        if confidences is not None:
            conf = int(confidences[i])

        # display prediciton
        if yp == 1:
            print "Prediction: ", data.teamAList[i], " over ", \
                    data.teamBList[i], "(", conf, ")\n"
        else:
            print "Prediction: ", data.teamBList[i], " over ", \
                    data.teamAList[i], "(", conf, ")\n"


