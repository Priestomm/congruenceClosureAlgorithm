import networkx as nx
from parser import Parser
from node import Node
from pysmt.smtlib.parser import SmtLibParser
import itertools
import sys
import re
    
class CongruenceAlgorithm:

    def __init__(self, g: nx.Graph) -> None:
        self.g = g

    def node(self, i: int) -> Node:
        return self.g.nodes[i]['node']
    
     
    def find(self, i: int) -> Node:
        n = self.node(i)
        if n.find == i: return i
        else: return self.find(n.find)

    def union(self, i1: int, i2: int) -> None:
        n1 = self.node(self.find(i1))
        n2 = self.node(self.find(i2))
        n1.find = n2.find
        n2.ccpar = n1.ccpar.union(n2.ccpar)
        n1.ccpar = set()
    
    def ccpar(self, i: int) -> set:
        return self.node(self.find(i)).ccpar

    def congruent(self, i1: int, i2: int) -> bool:
        n1 = self.node(i1)
        n2 = self.node(i2)

        if n1.fn != n2.fn or len(n1.args) != len(n2.args):
            return False
        
        for i, _ in enumerate(n1.args):
            if self.find(n1.args[i]) != self.find(n2.args[i]):
                return False
            
        return True

    def merge(self, i1: int, i2: int) -> None:
        while(self.find(i1) != self.find(i2)):
            pi1 = self.ccpar(i1)
            pi2 = self.ccpar(i2)
            self.union(i1, i2)
            for terms in list(itertools.product(pi1, pi2)):
                t1, t2 = terms
                if self.find(t1) != self.find(t2) and self.congruent(t1, t2):
                    self.merge(t1, t2)

def run(graph: nx.Graph, clauses: str) -> str:
    myParser = Parser(graph)
    myAlgo = CongruenceAlgorithm(graph)
    eqSet, nonEqSet = myParser.splitEq(clauses)
    subtermSet = myParser.subtermsSet()
    forbiddenMerges = set()

    for pair in nonEqSet:
        firstTerm, secondTerm = pair
        firstNode= myParser.nodeFromString(firstTerm)
        secondNode = myParser.nodeFromString(secondTerm)
        forbiddenMerges.add((firstNode, secondNode))

    for pair in eqSet:
        firstTerm, secondTerm = pair
        firstId = myParser.nodeFromString(firstTerm).id
        secondId = myParser.nodeFromString(secondTerm).id
        if (firstId, secondId) in forbiddenMerges:
            return "UNSAT"
        myAlgo.merge(firstId, secondId)
    
    for pair in nonEqSet:
        firstTerm, secondTerm = pair
        firstNode= myParser.nodeFromString(firstTerm)
        secondNode = myParser.nodeFromString(secondTerm)
        forbiddenMerges.add((firstNode, secondNode))
        if firstNode.find == secondNode.find:
            return "UNSAT"
    
    return "SAT"
        

def main(): 
    G = nx.Graph()
    prsr = Parser(G)

    script = SmtLibParser().get_script_fname(filename)
    f = script.get_strict_formula().serialize().__str__()[1:-1]
    f = f.replace(' ', '')

    #f = "(f(x0)=f(y)) & (x0!=y)"
    prsr.parse(f)
    print(run(G, f))

    for node in G.nodes():
        print(G.nodes[node]['node'])
    print(G.edges())

if __name__ == "__main__":
	main()	

