#
# Nome: Fasta.py
# Função: Facilitar leitura de arquivos fasta.
# Data: 01/06/2024
#

def getFastaFileSequence(inputFilePath: str):
    fastaFile = __tryOpenFile(inputFilePath)
    if fastaFile == "FILE_NOT_FOUND_EXCEPTION": return "FILE_NOT_FOUND_EXCEPTION"

    fastaData = fastaFile.readlines()
    checkFormatExceptions = __checkIfHasFastaFormat(fastaData)
    if "EXCEPTION" in checkFormatExceptions: return checkFormatExceptions

    fastaSequence = ''
    for line in fastaData:
        if line[0] != ">":
            if not __sequenceHasOnlyLetters(line): return "WRONG_FASTA_FORMAT_EXCEPTION"
            fastaSequence += line.strip()

    fastaFile.close()
    return fastaSequence


def makeFastaFile(firstSequence, secondSequence):
    outputFile = open('alinhamento_saida.fasta', 'w')
    for linha in firstSequence:
        outputFile.write(linha + '\n')
    for linha in secondSequence:
        outputFile.write(linha + '\n')
    outputFile.close

# FUNÇÕES PRIVADAS

def __checkIfHasFastaFormat(fastaData):
    if __isEmptyFile(fastaData):
        return "EMPTY_FILE_EXCEPTION"

    elif not __hasFastaFormat(fastaData):
        return "WRONG_FASTA_FORMAT_EXCEPTION"
    
    else:
        return "HAS_HEADER_AND_SEQUENCE"


def __tryOpenFile(filePath):
    try:
       inputFile = open(filePath)
       return inputFile
    except FileNotFoundError:
       return "FILE_NOT_FOUND_EXCEPTION"


def __isEmptyFile(fileData):
    hasLines = len(fileData) >= 1
    hasWords = False
    if hasLines:
        hasWords = len(fileData[0]) >= 1
    return not (hasLines and hasWords)


def __hasFastaFormat(fastaFile):
    hasSequence = len(fastaFile) >= 2
    hasHeader = fastaFile[0][0] == ">"
    return hasHeader and hasSequence
    

def __sequenceHasOnlyLetters(fastaSequence):
    return fastaSequence.strip().isalpha()