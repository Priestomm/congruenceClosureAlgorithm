# congruenceClosureAlgorithm
The repository contains an implementation in python of the Congruence Closure Algorithm for the (un)satisfiability problem explained in "Aaron R. Bradley and Zohar Manna. The calculus of computation".

## How to run the code
The project is very simple to run, the main.py file contains the algorithm and the script that allows to test it.

Here's some important things:
1. Choose if you want to write your own set of clauses or to test the algorithm with a bunch of test files I provided, by selecting (Y/N)
2. Type your set of clauses or select a number between 1 and 6 (included)
3. Check if the set is SAT or UNSAT
   
## Format of the input
In case you wanted to write the clauses this is the format you have to follow:
* The symbol for equality is "="
* The symbol for disequality is "!="
* A single clause is closed in round brackets --> (f(a)=f(b))
* The different clauses have to be separeted with "&" --> (f(a)=f(b)) & (a!=b)
* Spaces won't affect the string
* You can use both infix and prefix notation for inequality --> (!(a=b)) is equal to (a!=b)

## Colab
I also provide a Notepad which you can run form Google Colab:

https://colab.research.google.com/drive/1SDn87isTnpuXMle48LcmEBBP2pEMwqW5?usp=sharing
