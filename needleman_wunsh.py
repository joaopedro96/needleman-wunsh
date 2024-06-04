import numpy as np
import pandas as pd
from IPython.display import display
from Lib import Blosum
from Lib import Fasta


def getDataFromTempFile():
    tempFile = open('temp.txt')
    fileData = tempFile.readlines()
    tempFile.close()
    return fileData


def getSequencesFromPaths(firstPath, secondPath):
    firstSequence = Fasta.getFastaFileSequence(firstPath)
    secondSequence = Fasta.getFastaFileSequence(secondPath)

    if 'EXCEPTION' in firstSequence:
        handleException(firstSequence)
    
    elif 'EXCEPTION' in secondSequence:
        handleException(secondSequence)

    else:
        return (firstSequence, secondSequence)


def handleException(exceptionName):
    tempFile = open('temp.txt', 'w')
    tempFile.write(exceptionName)
    tempFile.close
    exit()


def getEmptyScoreMatrix(firstSequence, secondSequence):
    rowQuantity = len(firstSequence) + 1
    collumnQuantity = len(secondSequence) + 1
    zeroMatrix = np.zeros((rowQuantity, collumnQuantity), dtype=int)
    return zeroMatrix


def getEmptyPathMatrix(firstSequence, secondSequence):
    rowQuantity = len(firstSequence) + 1
    collumnQuantity = len(secondSequence) + 1

    emptyMatrix = []
    for row in range(rowQuantity):
        newRow = []
        for collumn in range(collumnQuantity):
            newRow.append('')
        emptyMatrix.append(newRow)

    return emptyMatrix


def getMatrixValues(firstSequence, secondSequence, gapPenalty, selectedBlosum):
    scoreMatrix = getEmptyScoreMatrix(firstSequence, secondSequence)
    pathMatrix = getEmptyPathMatrix(firstSequence, secondSequence)
    rows = len(firstSequence) + 1
    collumns = len(secondSequence) + 1

    for rowIndex in range(1, rows):
        for collumnIndex in range(1, collumns):
            matchScore = Blosum.getMatchScore(selectedBlosum, firstSequence[rowIndex - 1], secondSequence[collumnIndex - 1])

            diagScore = scoreMatrix[rowIndex - 1][collumnIndex - 1] + matchScore
            upScore = scoreMatrix[rowIndex - 1][collumnIndex] - gapPenalty
            leftScore = scoreMatrix[rowIndex][collumnIndex - 1] - gapPenalty

            bestScore = max(diagScore, upScore, leftScore)
            scoreMatrix[rowIndex][collumnIndex] = bestScore

            if bestScore == diagScore:
                pathMatrix[rowIndex][collumnIndex] = "↖"

            elif bestScore == upScore:
                pathMatrix[rowIndex][collumnIndex] = '↑'
            
            else:
                pathMatrix[rowIndex][collumnIndex] = '←'
    
    return (scoreMatrix, pathMatrix)


def getGlobalAlignment(firstSequence, secondSequence, pathMatrix):
    firstSeqAlign = ''
    secondSeqAlign = ''
    rowIndex = len(firstSequence)
    collumnIndex = len(secondSequence)

    while (rowIndex != 0) and (collumnIndex != 0):
        if pathMatrix[rowIndex][collumnIndex] == '↖':
            firstSeqAlign += firstSequence[rowIndex - 1]
            secondSeqAlign += secondSequence[collumnIndex - 1]
            rowIndex -= 1
            collumnIndex -= 1
        
        elif pathMatrix[rowIndex][collumnIndex] == '↑':
            firstSeqAlign += firstSequence[rowIndex - 1]
            secondSeqAlign += "-"
            rowIndex -= 1      

        elif pathMatrix[rowIndex][collumnIndex] == '←':
            firstSeqAlign += "-"
            secondSeqAlign += secondSequence[collumnIndex - 1]
            collumnIndex -= 1   

    reversedFirstSeq = firstSeqAlign[::-1]
    reversedSecondSeq = secondSeqAlign[::-1]

    return (reversedFirstSeq, reversedSecondSeq)


def logTable(matrix, firstSequence, secondSequence):
    rowLabels = [label for label in '-' + firstSequence]
    collumnLabels = [label for label in '-' + secondSequence]
    formattedTable = pd.DataFrame(matrix, index=rowLabels, columns=collumnLabels)
    display(formattedTable)


#VARIAVEIS DE ENTRADA
tempFileData = getDataFromTempFile()
firstSequencePath = tempFileData[0].strip()
secondSequencePath = tempFileData[1].strip()
selectedBlosum = tempFileData[2].strip()
gapPenalty = int(tempFileData[3].strip())

#SEQUENCIAS A SEREM ALINHADAS
fastaSequencesData = getSequencesFromPaths(firstSequencePath, secondSequencePath)
firstSequence = fastaSequencesData[0]
secondSequence = fastaSequencesData[1]

#ALINHAMENTO DAS SEQUENCIAS
matrixList = getMatrixValues(firstSequence, secondSequence, gapPenalty, selectedBlosum)
scoreMatrix = matrixList[0]
pathMatrix = matrixList[1]
globalAlignedSequences = getGlobalAlignment(firstSequence, secondSequence, pathMatrix)

#IMPRESSÃO DE RESULTADOS
print('\nMatriz de pontuação:')
logTable(scoreMatrix, firstSequence, secondSequence)
print('\nMatriz de caminhos:')
logTable(pathMatrix, firstSequence, secondSequence)
print('\nSequencia V:')
print(globalAlignedSequences[0])
print('\nSequencia W:')
print(globalAlignedSequences[1])