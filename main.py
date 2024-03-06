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
    tables = []
    availableplayers = []
    for index in range(numPlayers):
        availableplayers.append(index)
    #Get tables
    for tableIndex in range(numTables):
        table = selectFourPlayersNeverMatched(availableplayers)
        #table = selectFourPlayers(availableplayers)
        addOpponentsToList(table) #Add playerMatchedWith chosen to the list
        tables.append(table)
    return tables

def selectFourPlayersNeverMatched(availableplayers):
    table = []
    for index in range(4):
        tries = 100
        areadyPlayedWith = True
        while areadyPlayedWith == True:
            tries -= 1
            if tries == 0:
                areadyPlayedWith = False
                continue
            
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

def addOpponentsToList(table):
    for playerIndex in table:
        for playerIndex2 in table:
            if(playerIndex != playerIndex2):
                playerMatchedWith[playerIndex].append(playerIndex2)

#The goal is to fix tables that player already played with with player that he never played with.
def fixPlayerOpponents(tables):

    #REFAIT TON PSEUDOCODE
    # On check tous les adversaires de l'adversaire pour voir s'il a un doublon
    # En cas de doublon, Il faut changer ce joueur de table
    # Si l'échange de l'adversaire ne pose aucun problème de son côté, on l'intervertis
    # Sinon, on tente de lui trouver une table où il n'a jamais joué avec les 3 autres joueurs
    # Si aucune table n'est possible, on ne fait rien et on attend une nouvelle relance
    
    # Loop on players
    for playerIndex in range(len(players) - 1):
        seen = set()
        unique = []
        # Check every opponent this player had
        for opponent in playerMatchedWith[playerIndex]:
            if opponent not in seen:
                #If unseen, does nothing but tracking it
                unique.append(opponent)
                seen.add(opponent)
            else:
                #If already battled, prepare to swipe the player with a table he never met anyone
                sessionNumber = int(len(unique) / 3)
                sessionTables = tables[sessionNumber]

                playerTableNumber = -1
                for tableNumber in range(len(sessionTables) -1):
                    if playerIndex in sessionTables[tableNumber]:
                        playerTableNumber = tableNumber
                        break


                for table in sessionTables:
                    if playerIndex in sessionTables: 
                        continue

                    canSwap = True
                    #Check if new table is ok for the player
                    for opponentIndex in table:
                        if opponentIndex in playerMatchedWith[playerIndex]:
                            canSwap = False

                    if canSwap:
                        #Check if new table is ok for the opponent
                        for playerIndex in sessionTables[tableNumber]:
                            if playerIndex in playerMatchedWith[opponent]:
                                canSwap = False

                    if canSwap:
                        #Swaps table
                        table.append(playerIndex)
                        sessionTables[playerTableNumber].append(opponent)

                        del table[table.index(opponent)]
                        del sessionTables[playerTableNumber][sessionTables[playerTableNumber].index(playerIndex)]
                        tables[sessionNumber] = sessionTables
                        return



def findInArray(array, value):
    indexValue = -1
    try:
        indexValue = array.index(value)
    except ValueError:
        indexValue = -1
    return indexValue

def writeAllInFile(sessionTables):
    file = open("testTables.txt", "w")
    
    sessionNumber = 0
    for sessionTable in sessionTables:
        sessionNumber += 1
        file.write("Session " + str(sessionNumber) + ": \n")
        for table in sessionTable:
            counter = 0
            for indexPlayer in table:
                if counter!=0: file.write("\t")
                file.write(str(players[indexPlayer])) # In the final file, we write correct player Number
                counter += 1
            file.write("\n")
        file.write("\n\n")
    file.close()



notGood = False
numSessions = 7
numPlayers = 40
numTables = int(numPlayers / 4)

players = []
playerMatchedWith = []
tournamentsSession = []
tables = []
sessionTables = []

    
initVars()
#printPlayersMatchedWith()
# 1. Setup sessions
for sessionNumber in range(numSessions):
    tables = setupSession(sessionNumber)
    sessionTables.append(tables)
    
# 2. Fix each players opponents
for index in range(10000):
    fixPlayerOpponents(sessionTables)

writeAllInFile(sessionTables)

print("Done!")