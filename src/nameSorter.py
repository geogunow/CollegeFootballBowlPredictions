import csv
from pprint import pprint

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


# run script
if __name__ == '__main__':
    teams = sortTrTeamNames()
    for team in teams:
        print team
