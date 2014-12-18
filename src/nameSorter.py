import csv
from pprint import pprint
from copy import deepcopy as copy
from featureExtractor import *
import numpy as np

"""
A function that cyclest through tream rankings data (tr) and finds all team
names. This function returns a sorted list of all team names it finds.
"""
def sortTrTeamNames():
   
    # initialize set and base file
    name_set = set()
    base_fname = '../Data/tr/complete/TOP/y'

    # cycle through all years
    for y in range(2003,2015):
        fname = base_fname + str(y)

        # open file to find all team names
        with open(fname,'r') as fh:

            # cycle through all lines in the file
            lines = fh.readlines()
            for line in lines:
                words = line.split('\t')

                # extract data, add to set
                rank = int(words[0])
                team = words[1]
                name_set.add(team)

    name_list = list(name_set)
    
    print name_list
    name_list = sorted(name_list)

    return name_list


"""
Prints all unique conferences
"""
def printConferences():

    conference_set = set()
    conferences = extractConferences()

    bowl_games = extractBowlResults()

    for game in bowl_games.values():
        for team in (game.teamA, game.teamB):
            conference = conferences[team][game.season]
            
            if conference not in conference_set:
                print conference
                conference_set.add(conference)


"""
Engineer features that are encapsulated in existing data
"""
def engineerFeatures(stats):

    # add engineered dictionaries
    stats['total_defense'] = dict()
    stats['total_offense'] = dict()
    stats['TO_margin'] = dict()

    for y in range(2003,2015):

        # form nested layer with year
        stats['total_defense'][y] = dict()
        stats['total_offense'][y] = dict()
        stats['TO_margin'][y] = dict()

        # cycle through teams to calculate statistics
        for team in stats['rushing_defense'][y].keys():
           
            # unpack stats
            rushing_def = stats['rushing_defense'][y][team]
            rushing_off = stats['rushing_offense'][y][team]
            passing_def = stats['passing_defense'][y][team]
            passing_off = stats['passing_offense'][y][team]
            give = stats['giveaways'][y][team]
            take = stats['takeaways'][y][team]
            pf = stats['points_for'][y][team]
            pa = stats['points_against'][y][team]

            # calculate length of lists
            nvals = len(pa)

            # initialize new variable arrays
            total_off = []
            total_def = []
            to_margin = []

            # calculate new features
            for i in xrange(1, nvals):

                total_def.append( passing_def[i] + rushing_def[i] )
                total_off.append( passing_off[i] + rushing_off[i] )
                to_margin.append( take[i] - give[i] )

            # add features to dictionary
            stats['total_defense'][y][team] = total_def
            stats['total_offense'][y][team] = total_off
            stats['TO_margin'][y][team] = to_margin


        new_stats = ['total_defense','total_offense','TO_margin']
        for stat in new_stats:
            
            values = copy(stats[stat][y].values())
            indexes = range(len(values))
            indexes.sort(key=values.__getitem__)
            
            ranks = np.zeros(len(values))
            if stat is 'total_defense':
                rank = 1
                for index in indexes:
                    ranks[index] = rank
                    rank += 1
            else:
                rank = len(indexes)
                for index in indexes:
                    ranks[index] = rank
                    rank -= 1

            # formulate lines to print
            lines = []
            for i, team in enumerate(stats[stat][y].keys()):
                line = ''
                line += str(int(ranks[i])) + '\t' + team
                
                # print attributes paying attention to missing data
                for j, attr in enumerate(stats[stat][y][team]):
                    if j == 2:
                        line += ( '\t' + '--' )
                    line += ( '\t' + str(attr) )
                line += ( '\t' + '--')
                
                # add line to lists of lines to print
                lines.append(line)

            # sort lines by rank
            zipped = dict(zip(lines, ranks))
            lines.sort(key=zipped.get)

            # print lines to new file
            fname = '../Data/tr/incomplete/' + stat + '/y' + str(y)
            with open(fname,'w') as fh:
                for line in lines[:-1]:
                    fh.write(line + '\n')
                fh.write(lines[-1])


# run script
if __name__ == '__main__':
    #teams = sortTrTeamNames()
    #for team in teams:
    #print team

    #stats = formTrStatistics()
    printConferences()
