import networkx as nx
from parser import Parser
from node import Node
import itertools
import re
    
class congruenceAlgorithm:

    def __init__(self, g: nx.Graph) -> None:
        self.g = g

    def node(self, i: int) -> Node:
        for node in self.g.nodes():
            if node.id == i:
                return node
        return None
     
    def find(self, i: int) -> Node:
        n = self.node(i)
        if n.find == i: return i
        else: return self.find(n.find)

    def union(self, i1: int, i2: int) -> None:
        n1 = self.node(i1)
        n2 = self.node(i2)
        n1.find = n2.find
        n2.ccpar = n1.ccpar.union(n2.ccpar)
        n1.ccpar = set()
    
    def ccpar(self, i: int) -> set:
        return self.node(self.fin(i)).ccpar

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

        

def main(): 
    G = nx.Graph()
    algorithm = congruenceAlgorithm(G)
    prsr = Parser(G)

    clauses = "f(f(f(a)))=a & f(f(f(f(f(a)))))=a & f(a)=a "
    graph = prsr.parse(clauses)

    for node in graph.nodes():
        print(graph.nodes[node]['node'])
    print(graph.edges())

if __name__ == "__main__":
	main()	

