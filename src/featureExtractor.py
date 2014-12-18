import csv
from pprint import pprint
import numpy as np
import os

"""
A struct to store bowl game information
"""
class gameResult(object):
    def __init__(self, teamA, teamB, ptsA, ptsB, resultA, name, season):
        self.teamA = teamA
        self.teamB = teamB
        self.ptsA = ptsA
        self.ptsB = ptsB
        self.resultA = resultA
        self.name = name
        self.season = season

"""
A struct to store college football data set information
"""
class dataSet(object):
    def __init__(self):
        self.X = []
        self.Y = []
        self.teamAList = []
        self.teamBList = []
        self.yearList = []
        self.nameList = []

"""
A funciton that searches through bowl games, accepting those from 2003-2004
onward and returns a gameResult struct associated with each bowl game
"""
def extractBowlResults():

    # list of relevant bowl games
    gameList = dict()

    # search through bowl games file
    with open('../Data/bowlGames.csv','r') as csvfile:
        
        reader = csv.reader(csvfile, skipinitialspace = True)
        header = reader.next()
        
        for line in reader:
            
            # extract information
            date = line[3]
            season = findSeason(date)
            
            # determine if game is 2003-2004 season onward
            if season >= 2003:

                # extract information
                ptsA = int(line[4])
                teamB = line[5]
                ptsB = int(line[6])
                name = line[7]
                teamA = line[8]
                if ptsA > ptsB:
                    resultA = 1
                else:
                    resultA = 0

                # create game structure and key
                game = gameResult(teamA,teamB,ptsA,ptsB,resultA,name,season)
                key = name + ' ' + str(season)
                
                if key not in gameList:
                    gameList[key] = game
                    # pprint (vars(game))

    return gameList.values()

"""
A function that extracts matchups for coming bowl games
"""
def extractNewBowls():
    
    season = 2014
    gameList = []
    fname = '../bowls2014_locked'
    
    # open file to read lines
    with open(fname,'r') as fh:
        lines = fh.readlines()

        # cycle through all bowls
        for line in lines:

            # unpack data
            line = line.split('\n')
            line = line[0]
            data = line.split('\t')
            name = data[0]
            teamA = data[1]
            teamB = data[2]

            # add bowl game to list
            game = gameResult(teamA, teamB, None, None, None, name, season)
            gameList.append(game)

    return gameList

"""
A function that takes a data input in format 'MM-DD-YYYY' and converts it into
a college football season.  A season is taken to be defined by the starting
year. For instance, a bowl game in the 2003-2004 seaoson would return 2003.
"""
def findSeason(date):
    
    # split date into month, date, and year
    vals = date.split('-')
    m = int(vals[0])
    d = int(vals[1])
    y = int(vals[2])

    # correct games played in january
    if m == 1:
        y -= 1

    return y

"""
Extract naming dictionary for college football team names from csv name
associations file. This dicitonary maps a name in the bolw list to a name
in team rankings (tr).
"""
def extractTrNaming():
    
    # dictionary of team name associations
    nameDict = dict()

    # search through bowl games file
    with open('../Data/teamNamesMerge.csv','r') as csvfile:
        
        # read file and extract header
        reader = csv.reader(csvfile, skipinitialspace = True)
        header = reader.next()
        
        # cycle through lines
        for line in reader:

            # extract information
            name = line[0]
            tr = line[-1]

            # add to dictionary
            nameDict[name] = tr
             
    return nameDict

"""
Extract naming dictionary for college football team names from csv name
associations file. This dicitonary maps a name from the current bowl pickem
by James Sparks to a name in team rankings (tr).
"""
def extractTrJamesNaming():
    
    # dictionary of team name associations
    nameDict = dict()

    # search through bowl games file
    with open('../Data/teamNamesMerge.csv','r') as csvfile:
        
        # read file and extract header
        reader = csv.reader(csvfile, skipinitialspace = True)
        header = reader.next()
        
        # cycle through lines
        for line in reader:

            # extract information
            name = line[-2]
            tr = line[-1]

            # add to dictionary
            nameDict[name] = tr
             
    return nameDict

"""
Extract naming dictionary for college football team names from csv name
associations file. This dicitonary maps a name from the current bowl pickem
by James Sparks to the original name.
"""
def reverseJamesNaming():
    
    # dictionary of team name associations
    nameDict = dict()

    # search through bowl games file
    with open('../Data/teamNamesMerge.csv','r') as csvfile:
        
        # read file and extract header
        reader = csv.reader(csvfile, skipinitialspace = True)
        header = reader.next()
        
        # cycle through lines
        for line in reader:

            # extract information
            name = line[-2]
            orig = line[0]

            # add to dictionary
            nameDict[name] = orig
             
    return nameDict


"""
Function that returns a dictionary of team statistics form tream rankings (tr)
"""
def formTrStatistics():
    
    # create dictionary for statistics
    stats = dict()

    # find categories
    file_base = '../Data/tr/complete'
    tree = os.walk(file_base)
    root, categories, files = tree.next()

    # iterate through all categories
    for category in categories:
        stats[category] = dict()

        # iterate through all years
        for y in range(2003,2015):
            stats[category][y] = dict()
            fname = file_base + '/' + category + '/y' + str(y)

            # load stats from file
            with open(fname,'r') as fh:
                lines = fh.readlines()

                # iterate through all teams
                for line in lines:
                   
                    data = line.split('\t')
                    
                    # make sure line is not empty
                    if len(line) > 1:
                        
                        # unpack data
                        rank = int(data[0])
                        team, record = getTeamName(data[1])
                        value = getFloatValue(data[2])

                        # add data to diciontary
                        if record is None:
                            
                            # unpack more data
                            last3 = dataImputeFloat(value, data[3])
                            last1 = dataImputeFloat(value, data[4])
                            home = dataImputeFloat(value, data[5])
                            away = dataImputeFloat(value, data[6])

                            stats[category][y][team] = \
                                    [rank, value, last3, home, away]
                        
                        else:
                            # determine wins and losses
                            wins = int(record[0])
                            losses = int(record[1])
                            stats[category][y][team] = \
                                    [rank, value, wins, losses]
    return stats

"""
Check if float value is missing. In the current version this means that a 
sub category such as TOP in last 3 games is missing. For missing data we assign
the regular value. For example, we would assign TOP for the season (input as
value) since this is approximately the MLE guess. However, this is data
imputation, which is not rigorous and should be changed to EM.
"""
def dataImputeFloat(value, string):
    if string == '--':
        return value
    else:
        if string[-1] == '%':
            return float(string[0:-1])
        else:
            return float(string)


"""
Get the float of a string value. Check for a % sign and if it is present,
remove it.
"""
def getFloatValue(string):
    if string[-1] == '%':
        return float(string[0:-1])
    else:
        return float(string)

"""
From string input, determine if a record is included. If it is, return both
the team name and record. Otherwise, return the team name and "None"
"""
def getTeamName(string):
    
    index = string.rfind('(')

    if string[index+1].isdigit():
        name = string[:index-1]
        record_string = string[index+1:-1]
        record = record_string.split('-')
        return name, record
    else:
        return string, None


"""
Reads through College-Football-2013-11-04.csv to determine the conference of
each team for the relevant years (2003 and onward). 2014 data is missing so it
is pulled from 2013 with corrections made for Rutgers and Maryland
"""
def extractConferences():

    # list of relevant bowl games
    conferenceMapping = dict()

    # search through bowl games file
    with open('../Data/College-Football-2014-11-04.csv','r') as csvfile:
        
        reader = csv.reader(csvfile, skipinitialspace = True)
        header = reader.next()
        
        for line in reader:
            
            # extract year
            year = int(line[0])

            # determine if year is greater than 2003-2004 season onward
            if year >= 2003:
            
                # extract team and confernce
                team = line[4]
                conference = line[17]

                # load new team into dictionary if new
                if team not in conferenceMapping:
                    conferenceMapping[team] = dict()

                # add the year and conference information
                conferenceMapping[team][year] = conference

                # determine 2014 conference by carrying over from 2013
                if year == 2013:
                    conferenceMapping[team][2014] = conference

    return conferenceMapping

"""
Function that creates a list of feature vectors for each bowl game along with
a list of labels (win/loss) for previous bowl games.
"""
def formFeatureVectors(final = False):

    # initialize data set to store feature information such as features
    data = dataSet()

    # load statistics
    teamStats = formTrStatistics()

    # load conferences
    teamConferences = extractConferences()

    if final:
        reverseNaming = reverseJamesNaming()
    
    # load dictionary for team name associations
    if final: 
        trNames = extractTrJamesNaming()
    else:
        trNames = extractTrNaming()

    # get bowl games
    if final:
        bowls = extractNewBowls()
    else:
        bowls = extractBowlResults()

    # cycle through all recorded bowl games
    for game in bowls:

        if final:
            resultA = None
            resultB = None
        else:
            resultA = game.resultA
            resultB = 1-resultA

        # create team A features
        teamA = trNames[game.teamA]
        teamAFeatures = createTeamFeatures(teamStats, teamA, game.season,
                resultA)

        # create team B features
        teamB = trNames[game.teamB]
        teamBFeatures = createTeamFeatures(teamStats, teamB, game.season, 
                resultB)

        # get orignal team A and team B names
        teamAOrig = game.teamA
        teamBOrig = game.teamB
        
        # if final dataset, correct names
        if final:
            teamAOrig = reverseNaming[teamAOrig]
            teamBOrig = reverseNaming[teamBOrig]

        # add conference for tream A
        conference = teamConferences[teamAOrig][game.season]
        teamAConference = createConferenceFeatures( conference )

        # add conference for tream B
        conference = teamConferences[teamBOrig][game.season]
        teamBConference = createConferenceFeatures( conference )

        #TODO: add distance feature by game name, team names

        # form total feature vector
        featureVector = teamAFeatures + teamBFeatures + teamAConference +\
                teamBConference

        # append feature vector to list (Xdata)
        data.X.append(featureVector)

        if not final:
            # append outcome to Ydata
            data.Y.append(game.resultA)

        # form lists of teamA, teamB, year
        data.teamAList.append(teamA)
        data.teamBList.append(teamB)
        data.yearList.append(game.season)
        data.nameList.append(game.name)

    return data

"""
Function that looks up statistics of a given team for a given year. It returns
a list of appropriate features to be used in the machine learning algorithm.
"""
def createTeamFeatures(teamStats, team, year, result):
    features = []
    for category in teamStats.keys():
        categoryFeatures = teamStats[category][year][team]
        if len(categoryFeatures) == 4:
            if result == 1:
                categoryFeatures[-2] -= 1
            elif result == 0:
                categoryFeatures[-1] -= 1
        
        features = features + categoryFeatures

    return features

"""
Checks the conference and makes a categorical feature which is represented
as 13 binary features (13 possible categories)
"""
def createConferenceFeatures(conference):
    conferences = ['Atlantic Coast Conference',
                    'Big East Conference',
                    'Big 12 Conference',
                    'Big Ten Conference',
                    'Pacific-12 Conference',
                    'Mountain West Conference',
                    'Division I-A Independent',
                    'Mid-American Conference',
                    'Sun Belt Conference',
                    'Western Athletic Conference',
                    'Conference USA',
                    'Southeastern Conference',
                    'American Athletic Conference']

    featureVector = []
    for test_conference in conferences:
        
        # test if conference is correct
        if conference == test_conference:
            featureVector.append(1)
            alarm = False
        else:
            featureVector.append(0)

    return featureVector


