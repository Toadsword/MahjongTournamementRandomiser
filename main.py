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
playerMatchedWith = []
tournamentsSession = []

file = open("testTables.txt", "w")

def initVars():
    for index in range(1, numPlayers + 1): #Player numbers
        players.append(index)
        playerMatchedWith.append([])
    random.shuffle(players)

def printPlayersMatchedWith():
    for index in range(numPlayers): #Player indexs
        print(str(players[index]) + " : " + str(playerMatchedWith[index]))

def setupSession(sessionNumber):
    availableplayers = []
    #init
    print("Session number : " + str(sessionNumber))
    file.write("Session " + str(sessionNumber) + ": \n")
    for index in range(numPlayers):
        availableplayers.append(index)
    #file.write(str(availableplayers) + "\n")
    #file.write(str(players) + "\n")
    #Get tables
    for tableIndex in range(numTables):
        table = selectFourPlayersNeverMatched(availableplayers)
        file.write("\n")
        addOpponentsToList(table) #Add playerMatchedWith chosen to the list
    file.write("\n\n")

def selectFourPlayersNeverMatched(availableplayers):
    table = []
    for index in range(4):
        selectedPlayerIndex = random.randint(0, len(availableplayers) - 1)
        #selectedPlayerIndex = len(availableplayers) -1
        #To add the player, their opponents must not be in the current table.
        for indexTable in table:
            for opponentPlayerId in playerMatchedWith[selectedPlayerIndex]:
                if opponentPlayerId == players[indexTable]:
                    selectedPlayerIndex -= 1
        


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
                playerMatchedWith[playerIndex].append(players[playerIndex2])

def findInArray(array, value):
    indexValue = -1
    try:
        indexValue = array.index(value)
    except ValueError:
        indexValue = -1
    return indexValue
    
initVars()
#printPlayersMatchedWith()
for sessionNumber in range(numSessions):
    setupSession(sessionNumber)
    printPlayersMatchedWith()


file.close()