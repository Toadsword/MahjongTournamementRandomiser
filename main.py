# Mahjong random tables generator

# This python script is designed to randomise and select oponents for each players
# This program is designed without considering teams

# Here are the rules the program must follow for the random to be correct :
# 1. Not two matches against the same oponent
# 2. Every players must be assigned a table for each sessions

# We're writing player number in the file, but work with player indexs the rest of the time

import random

numSessions = 7
numPlayers = 40
numTables = int(numPlayers / 4)

players = []
opponents = []
tournamentsSession = []

file = open("testTables.txt", "w")

def initVars():
    for index in range(1, numPlayers + 1): #Player numbers
        players.append(index)
        opponents.append([])
    random.shuffle(players)

def printPlayersAndOpponents():
    for index in range(numPlayers): #Player indexs
        print(str(players[index]) + " : " + str(opponents[index]))

def setupSession():
    availableplayers = []
    #init
    file.write("Session 1 : \n")
    for index in range(numPlayers):
        availableplayers.append(index)
    file.write(str(availableplayers) + "\n")
    file.write(str(players) + "\n")

    #Get tables
    for tableIndex in range(numTables):
        table = selectFourPlayersNeverMatched(availableplayers)
        file.write("\n")
        addOpponentsToList(table) #Add opponents chosen to the list

def selectFourPlayersNeverMatched(availableplayers):
    table = []
    for index in range(4):
        selectedPlayerIndex = random.randint(0, len(availableplayers) - 1)
        table.append(availableplayers[selectedPlayerIndex])
        file.write(str(players[availableplayers[selectedPlayerIndex]])) # In the final file, we write correct player Number
        if index!=3: file.write("\t")
        del availableplayers[selectedPlayerIndex]

    print("new AvailablePlayers : " + str(availableplayers))
    print("table : " + str(table))
    return table

def addOpponentsToList(table):
    for playerIndex in table:
        for playerIndex2 in table:
            if(playerIndex != playerIndex2):
                opponents[playerIndex].append(playerIndex2)

    
initVars()
#printPlayersAndOpponents()
setupSession()


file.close()