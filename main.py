# Mahjong random tables generator

# This python script is designed to randomise and select oponents for each players
# This program is designed without considering teams

# Here are the rules the program must follow for the random to be correct :
# 1. Not two matches against the same oponent
# 2. Every players must be assigned a table for each sessions

# We're writing player number in the file, but work with player indexs the rest of the time

import random

def initVars():
    for index in range(1, numPlayers + 1): #Player numbers
        players.append(index)
        playerMatchedWith.append([])

    #random.shuffle(players)

def printPlayersMatchedWith():
    for index in range(numPlayers): #Player indexs
        print(str(players[index]) + " : " + str(playerMatchedWith[index]))

def setupSession(sessionNumber):
    #init
    #print("Session number : " + str(sessionNumber))
    file.write("Session " + str(sessionNumber) + ": \n")

    attempts = 0
    retry = True
    while retry:
        if attempts > 100:
            return False
        
        retry = False
        tables = []
        availableplayers = []
        for index in range(numPlayers):
            availableplayers.append(index)
        #Get tables
        for tableIndex in range(numTables):
            #table = selectFourPlayersNeverMatched(availableplayers)
            table = selectFourPlayers(availableplayers)
            if len(table) != 4: 
                attempts += 1
                retry = True
                break 
            tables.append(table)
        
        for table in tables:
            file.write("\n")
            counter = 0
            for indexPlayer in table:
                if counter!=0: file.write("\t")
                file.write(str(players[indexPlayer])) # In the final file, we write correct player Number
                counter += 1
                
            addOpponentsToList(table) #Add playerMatchedWith chosen to the list
    file.write("\n\n")
    return True

def selectFourPlayersNeverMatched(availableplayers):
    tries = 100
    table = []
    for index in range(4):
        areadyPlayedWith = True
        while areadyPlayedWith == True:
            tries -= 1
            if tries == 0:
                return table
            
            selectedPlayerIndex = random.randint(0, len(availableplayers) - 1)

            areadyPlayedWith = False
            if len(table) > 0:
                for indexTable in table:
                    try:
                        #Check if we find the player in the opponent list
                        indexed = playerMatchedWith[availableplayers[selectedPlayerIndex]].index(indexTable)
                        areadyPlayedWith = True
                    except:
                        #Will return an error if it doesn't find it, so we go away with the selectedPlayerIndex
                        continue
            else:
                areadyPlayedWith = False
                
        table.append(availableplayers[selectedPlayerIndex])
        del availableplayers[selectedPlayerIndex]

    #print("new AvailablePlayers : " + str(availableplayers))
    #print("table : " + str(table))
    return table

def selectFourPlayers(availableplayers):
    table = []
    for index in range(4):
        selectedPlayerIndex = random.randint(0, len(availableplayers) - 1)            
        table.append(availableplayers[selectedPlayerIndex])
        del availableplayers[selectedPlayerIndex]
    

    return table

def addOpponentsToList(table):
    for playerIndex in table:
        for playerIndex2 in table:
            if(playerIndex != playerIndex2):
                playerMatchedWith[playerIndex].append(playerIndex2)

def findInArray(array, value):
    indexValue = -1
    try:
        indexValue = array.index(value)
    except ValueError:
        indexValue = -1
    return indexValue


notGood = True
attemptNumber = 0
file = open("testTables.txt", "w")
while notGood:
    attemptNumber += 1
    file.close()
    file = open("testTables.txt", "w")

    notGood = False
    numSessions = 7
    numPlayers = 40
    numTables = int(numPlayers / 4)

    players = []
    playerMatchedWith = []
    tournamentsSession = []

        
    initVars()
    #printPlayersMatchedWith()
    for sessionNumber in range(numSessions):
        if setupSession(sessionNumber) == False:
            notGood = True
            print(str(attemptNumber) + ": stopped at session : " + str(sessionNumber + 1))
            break
            #printPlayersMatchedWith()

    print("Done!")
    file.close()