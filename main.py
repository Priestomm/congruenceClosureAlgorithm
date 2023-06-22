import networkx as nx
from parser import Parser
from node import Node
from pysmt.smtlib.parser import SmtLibParser
import matplotlib.pyplot as plt
import itertools
    
class CongruenceAlgorithm:

    def __init__(self, G: nx.DiGraph) -> None:
        self.G = G

    def node(self, i: int) -> Node:
        return self.G.nodes[i]['node']
    
     
    def find(self, i: int) -> Node:
        n = self.node(i)
        if n.find == i: return i
        else: return self.find(n.find)

    def union(self, i1: int, i2: int) -> None:
        n1 = self.node(self.find(i1))
        n2 = self.node(self.find(i2))
        if len(n1.ccpar) < len(n2.ccpar):
            n1.find = n2.find
            n2.ccpar = n1.ccpar.union(n2.ccpar)
            n1.ccpar = set()
        else:
            n2.find = n1.find
            n1.ccpar = n2.ccpar.union(n1.ccpar)
            n2.ccpar = set()
    
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

def run(G: nx.DiGraph, clauses: str) -> str:
    myParser = Parser(G)
    myAlgo = CongruenceAlgorithm(G)
    eqSet, nonEqSet = myParser.splitEq(clauses)
    subtermSet = myParser.subtermsSet()
    forbiddenMerges = set()

    # Forbidden List implementation
    for pair in nonEqSet:
        firstTerm, secondTerm = pair
        firstNode= myParser.nodeFromString(firstTerm)
        secondNode = myParser.nodeFromString(secondTerm)
        forbiddenMerges.add((firstNode, secondNode))

    # Run the algorithm
    for pair in eqSet:
        firstTerm, secondTerm = pair
        firstId = myParser.nodeFromString(firstTerm).id
        secondId = myParser.nodeFromString(secondTerm).id
        if (firstId, secondId) in forbiddenMerges:
            return "UNSAT"
        myAlgo.merge(firstId, secondId)
    
    # Check for (un)satisfiability
    for pair in nonEqSet:
        firstTerm, secondTerm = pair
        firstNode= myParser.nodeFromString(firstTerm)
        secondNode = myParser.nodeFromString(secondTerm)
        forbiddenMerges.add((firstNode, secondNode))
        if firstNode.find == secondNode.find:
            return "UNSAT"
    
    return "SAT"

def drawGraph(G: nx.DiGraph):
    # Draw the graph
    pos = nx.circular_layout(G)
    nx.draw(G, pos=pos, with_labels=True)

    # Add node labels
    labels = nx.get_node_attributes(G, 'node')
    for node, label in labels.items():
        plt.annotate(label.fn, (pos[node][0], pos[node][1] + 0.05))

    # Display the graph
    plt.show()

def main():

    G = nx.DiGraph()
    prsr = Parser(G)

    while(True):
        choice = input("Do you want to write your own set of clauses? (Y/N) ")
        if choice in ["Y", "N"]: break
        print("Wrong answer, retry")

    if choice == "Y":
        f = input("Write your own set of clauses below\nRemember to use & to divide (in)equalities and != as a symbol for inequality and to embrace the clauses into round brackets \n").replace(' ','')
    elif choice == "N":
        test = input("Choose between 6 different tests: (1-6) ")
        filename = "tests/test" + str(test) + ".smt2"
        script = SmtLibParser().get_script_fname(filename)
        f = script.get_strict_formula().serialize().__str__()[1:-1]
        print("You selected: ", f)
        f = f.replace(' ','')

    prsr.parse(f)
    print("Your set is -->", run(G, f))

    drawGraph(G)
    

#    for node in G.nodes():
#        print(G.nodes[node]['node'])
#    print(G.edges())

if __name__ == "__main__":
	main()	

