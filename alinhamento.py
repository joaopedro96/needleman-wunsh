#
# Nome: alinhamento.py
# Função: Alinha globalmente duas sequencias 'V' e 'W'.
# Data: 01/06/2024
#

import sys
import os


def logHelpInstructions():
   print("""
    SCRIPT PARA ALINHAMENTO GLOBAL
         
    Descrição:
         
         Dado duas sequências 'V' e 'W' este script calculará o alinhamento global conforme pontuação de BLOSUM. 
         
    Instruções:
         
         * Para executar este script é necessário que as duas sequências de entrada estejam em arquivos únicos em formato fasta.
         * Utilize os argumentos '-v' e '-w' para informar o caminho destas sequências salvas em seu computador.
         * Este script tem como valor padrão uma penalidade de gap equivalente a '1 ponto' e utiliza o modelo de blocos de substituição
           por matriz 'BLOSUM62'. Para alterar os valores defaults do script utilize os comandos '-g' para definir uma nova pontuação de gap 
           e '-m' para especificar outra matriz BLOSUM.

    Uso:

        python3 alinhamento.py -v <primeira_sequencia.fasta> -w <segunda_sequencia.fasta>

    Comandos:

        -v --sequenceV      Caminho do arquivo fasta da primeira sequência
        -w --sequenceW      Caminho do arquivo fasta da segunda sequência
        -g --gapPenalty     Pontuação de penalidade para gaps (fornecer números inteiros). Valor padrão '1'.
        -m --blosumMatrix   Matriz de pontuação BLOSUM a ser utilizada (45, 62 ou 80). Valor padrão '62'.
        -h --help           Lista de instruções para uso deste script
    """
   )


def readInputArguments():
   for index, arg in enumerate(sys.argv):
      if index % 2 == 1:

         if arg == "-h" or arg == "--help":
            logHelpInstructions()
            exit()

         elif arg == "-v" or arg == "--sequenceV":
            global vSequencePath
            vSequencePath = getArgumentValue(index)
        
         elif arg == "-w" or arg == "--sequenceW":
            global wSequencePath
            wSequencePath = getArgumentValue(index)

         elif arg == "-g" or arg == "--gapPenalty":
            global gapPenalty
            gapPenalty = getArgumentValue(index)
            checkIfHasOnlyNumbers(gapPenalty)
            gapPenalty = abs(int(gapPenalty))

         elif arg == "-m" or arg == "--blosumMatrix":
            global blosumMatrix
            blosumMatrix = getArgumentValue(index)
            checkBlosumMatrixInputs(blosumMatrix)

         else:
            global unknownArg
            unknownArg = arg
            handleInputException(f"INPUT_UNKNOWN_COMMAND_EXCEPTION")


def getArgumentValue(index):
  try:
     return sys.argv[index + 1]
  except IndexError:
    handleInputException("VALUE_NOT_FOUND_IN_COMMAND_EXCEPTION")


def checkIfHasOnlyNumbers(input):
   if not input.isnumeric():
      handleInputException("WRONG_VARIABLE_TYPE_EXCEPTION")


def checkBlosumMatrixInputs(input):
   availableInputs = ['45', '62', '80']
   if input not in availableInputs:
      handleInputException("WRONG_BLOSUM_INPUT_EXCEPTION")


def checkVariableType(variable, variableType):
   if type(variable) is not variableType:
      handleInputException("WRONG_VARIABLE_TYPE_EXCEPTION")


def handleInputException(inputExceptionType):
    errorText = ""

    if inputExceptionType == "VALUE_NOT_FOUND_IN_COMMAND_EXCEPTION":
       errorText = "[!] Comando utilizado não apresenta nenhum valor."
    
    elif inputExceptionType == "WRONG_VARIABLE_TYPE_EXCEPTION":
        errorText = "[!] Tipo da variável utilizada incompativel."
    
    elif inputExceptionType == "WRONG_BLOSUM_INPUT_EXCEPTION":
        errorText = "[!] Valor da matriz BLOSUM incompativel."
    
    elif inputExceptionType == "INPUT_UNKNOWN_COMMAND_EXCEPTION":
       global unknownArg
       errorText = f"[!] Comando desconhecido: `{unknownArg}`"
       
    print(errorText)
    exit()


def checkExceptions():
   tempFile = open('temp.txt')
   tempFileData = tempFile.readline()
   tempFile.close()
   if 'EXCEPTION' in tempFileData:
      handleExceptionError(tempFileData.strip())


def handleExceptionError(exceptionName):
    errorText = ""
    if exceptionName == "FILE_NOT_FOUND_EXCEPTION":
       global vSequencePath
       global wSequencePath
       errorText = f"[!] Arquivo não encontrado: confira os caminhos de `{vSequencePath}` e `{wSequencePath}`."
       
    elif exceptionName == "EMPTY_FILE_EXCEPTION":
       errorText = "[!] Arquivo vazio: arquivo fasta de entrada não contem dados."

    elif exceptionName == "WRONG_FASTA_FORMAT_EXCEPTION":
       errorText ="[!] Erro de formato: conteudo do arquivo não apresenta formato fasta."

    print(errorText)
    print("\nScript finalizado com erros.")
    os.remove("temp.txt")
    exit()


def makeTemporaryFile():
   global vSequencePath
   global wSequencePath
   tempFile = open('temp.txt', 'w')
   tempFile.write(vSequencePath + '\n')
   tempFile.write(wSequencePath + '\n')
   tempFile.write(blosumMatrix + '\n')
   tempFile.write(str(gapPenalty))
   tempFile.close()


def runScript():
   os.system("python3 needleman_wunsh.py")
   checkExceptions()
   os.remove("temp.txt")


#VALORES PADRÕES DE INICIALIZAÇÃO DO SCRIPT
gapPenalty = 1
blosumMatrix = '62'

#EXECUÇÃO DO SCRIPT
readInputArguments()
makeTemporaryFile()
runScript()