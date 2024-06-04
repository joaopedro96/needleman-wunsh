<h1 align="center">
    Needleman-Wunsh Algorithm
</h1>


## ℹ️ About this script
This code intends to implement a one-to-one aminoacidic sequence alingment through the Needleman-Wunsh algorithm.
It is an algorithm based on dynamic programming and thus finds an optimal solution for the alingment problem.

The used scoring system is the BLOSUM (BLOcks SUbstitution Matrix) similarity matrix. It is given the posibility to choose which BLOSUM matrix 
suits best your dataset.

Use:
  - BLOSUM45 - for more related proteins
  - BLOSUM62 - midrange
  - BLOSUM80 - for distantly related proteins

Finally, you are also allowed to choose the best gap penalty to penalize more or less indels.

## 🚀 How to run
To run this script on command line you should simply type the following on the root directory of this project:
- python alinhamento.py -v <path_for_sequence_one> -w <path_for_sequence_two

## ⚙ Commands
All commands supported in this script are listed bellow:

-h --> show the instructions to run this script

-v --> the path for the first fasta file containing one of the aminoacidic sequence
  
-w --> the path for the second fasta file containing the other aminoacidic sequence
  - see example files on the "Examples" folder (seqV.fasta and seqW.fasta)

-m --> Choose the desired BLOSUM substitution matrix:
  - use '-m 45', '-m 62' or '-m 80' for BLOSUM45, BLOSUM62 and BLOSUM80, respectively.

-g --> choose your gap penalty 
  - use natural numbers as '1' or '2' for negative (-1 and -2) gap penalties.

## 🧐 Examples
You can use the fasta files in folder 'Examples' to run this script for testing purpouses. Type on command line:
- python alinhamento.py -v Examples/seqV.fasta -w Examples/seqW.fasta
  
The gap penalty and BLOSUM substitution matrix has a default value of 1 and BLOSUM62 respectively. If you want to override these defaults values 
you should run the command line as specified in the sections above. 

As an example, if you want a gap penalty of 3 and BLOSUM substitution matrix as BLOSUM45 you should use:
- python3 alinhamento.py -v Examples/seqV.fasta -w Examples/seqW.fasta -m 45 -g 3

  
