# Mahjong random tables generator

# This python script is designed to randomise and select oponents for each players
# This program is designed without considering teams

# Here are the rules the program must follow for the random to be correct :
# 1. Not two matches against the same oponent
# 2. Every players must be assigned a table for each sessions

# We're writing player number in the file, but work with player indexs the rest of the time

import random

def initVars():
    players.clear()
    playerMatchedWith.clear()
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
def fixPlayerOpponents():

    #REFAIT TON PSEUDOCODE
    # On check tous les adversaires de l'adversaire pour voir s'il a un doublon
    # En cas de doublon, Il faut changer ce joueur de table
    # Si l'échange de l'adversaire ne pose aucun problème de son côté, on l'intervertis
    # Sinon, on tente de lui trouver une table où il n'a jamais joué avec les 3 autres joueurs
    # Si aucune table n'est possible, on ne fait rien et on attend une nouvelle relance
    
    # Loop on players
    couldntFixNumber = 0
    for playerIndex in range(len(players)):
        seen = set()
        unique = []
        # Check every opponent this player had
        for opponent in playerMatchedWith[playerIndex]:
            if opponent not in seen:
                #If unseen, does nothing but tracking it
                unique.append(opponent)
                seen.add(opponent)
            else:
                #print("P" + str(playerIndex) + " already played against p" + str(opponent) + "... Let's fix")
                #If already battled, prepare to swipe the player with a table he never met anyone
                sessionNumber = int(len(unique) / 3)
                sessionTables = allTables[sessionNumber]

                # Getting the informations on the playerIndex
                playerCurrentTableNumber = getPlayerTableNumber(playerIndex, sessionTables)
                currentTable = sessionTables[playerCurrentTableNumber]

                #Let's try to get him a new table to play !
                newTableIndex = -1
                for newSessionTableForPlayer in sessionTables:
                    newTableIndex += 1
                    if playerIndex in newSessionTableForPlayer: #We skip its current table
                        continue

                    if not hasAlreadyPlayedWithAnyone(opponent, newSessionTableForPlayer):
                        for otherTablePlayer in newSessionTableForPlayer:
                            #We don't want to take a player that has already played with the current player
                            if otherTablePlayer not in playerMatchedWith[playerIndex]:
                                swapPlayers(sessionNumber, playerCurrentTableNumber, opponent, newTableIndex, otherTablePlayer)
                                return 1
                    
                    # Get one opponent to swap with. The swapped opponent must be okay with the new table
                    for opponentIndex in newSessionTableForPlayer:
                        continue
                        # Check if the opponent has already played with more than two of the players
                        # Choisir un joueur qui est ok avec la nouvelle table
                        alreadyMatchedPlayersOnNewTable = []
                    
                        for player in currentTable:
                            #If the player already matched with the new opponent, skip
                            if player in playerMatchedWith[opponent]:
                                alreadyMatchedPlayersOnNewTable.append(player)
                        
                        #Too many players to be matched with again, not interested
                        if len(alreadyMatchedPlayersOnNewTable) > 1:
                            continue

                        # Only one, check if this player can be swapped to the table
                        if len(alreadyMatchedPlayersOnNewTable) == 1:
                            #If he never played with any other player...
                            if not hasAlreadyPlayedWithAnyone(alreadyMatchedPlayersOnNewTable[0], newSessionTableForPlayer):
                                #WE DO BE SWAPPING
                                swapPlayers(sessionNumber, playerCurrentTableNumber, opponent, newTableIndex, alreadyMatchedPlayersOnNewTable[0])
                                return False

                        #If none, check for any player to be swapped to the new table
                        if len(alreadyMatchedPlayersOnNewTable) == 0:
                            #Checks for all players
                            for opponentIndex in newSessionTableForPlayer:
                                if not hasAlreadyPlayedWithAnyone(opponentIndex, newSessionTableForPlayer):
                                    swapPlayers(sessionNumber, playerCurrentTableNumber, opponent, newTableIndex, opponentIndex)
                                    return False
                couldntFixNumber += 1
    return couldntFixNumber

def swapPlayers(sessionIndex, tableIndex1, playerIndex1, tableIndex2, playerIndex2):
   
    if playerIndex1 in allTables[sessionIndex][tableIndex1] and playerIndex2 in allTables[sessionIndex][tableIndex2]:

        #Swap player table
        allTables[sessionIndex][tableIndex1].append(playerIndex2)
        allTables[sessionIndex][tableIndex2].append(playerIndex1)
        
        allTables[sessionIndex][tableIndex1].remove(playerIndex1)
        allTables[sessionIndex][tableIndex2].remove(playerIndex2)

        #Recalculate all opponents
        calculateAllOpponents()
        print("Swapped players : session " + str(sessionIndex) + " :  Player " + str(playerIndex1) + " with player " + str(playerIndex2) + " between table " + str(tableIndex1) + " and " + str(tableIndex2))


def getPlayerTableNumber(playerIndex, sessionTables):
    for tableNumber in range(len(sessionTables)):
        if playerIndex in sessionTables[tableNumber]:
            return tableNumber
    raise Exception("Player is not in any table wtf")

def hasAlreadyPlayedWithAnyone(playerIndex, table):
    for opponent in table:
        if opponent in playerMatchedWith[playerIndex]:
            return True
    return False

def findInArray(array, value):
    indexValue = -1
    try:
        indexValue = array.index(value)
    except ValueError:
        indexValue = -1
    return indexValue

def calculateAllOpponents():
    playerMatchedWith.clear()
    
    for index in range(numPlayers): #Player numbers
        playerMatchedWith.append([])

    for session in allTables:
        for table in session:
            addOpponentsToList(table)

def writeAllInFile(sessionTables, fileName):
    file = open(fileName + ".txt", "w")
    
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


attempts = 0
while attempts < 30:
    attempts += 1
    print("Attempt " + str(attempts))

    notGood = False
    numSessions = 7
    numPlayers = 40
    numTables = int(numPlayers / 4)

    players = []
    playerMatchedWith = []
    allTables = []

    initVars()
    #printPlayersMatchedWith()
    # 1. Setup sessions  
    leftToFix = 0
    for sessionNumber in range(numSessions):
        sessionTable = setupSession(sessionNumber)
        allTables.append(sessionTable)
        calculateAllOpponents()
        for index in range(100):
            leftToFix = fixPlayerOpponents()
            if leftToFix == 0:
                print("EVERYTHING IN SESSION " + str(sessionNumber) + " IS CLEAR")
                break

    # 2. Fix each players opponents
    for index in range(100):
        leftToFix = fixPlayerOpponents()
        if leftToFix == 0:
            print("EVERYTHING IS FUCKING FIXED")
            break
            
    print("Left to fix : " + str(leftToFix))

    writeAllInFile(allTables, "AfterFix")

    if leftToFix == 0:
        print("Done in " + str(attempts) + " attempts!")
        break