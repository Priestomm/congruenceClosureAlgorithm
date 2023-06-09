from pyparsing import nestedExpr
from node import Node
import networkx as nx
import matplotlib.pyplot as plt

class Parser:

    def __init__(self, graph: nx.DiGraph) -> None:
        self.myParser = nestedExpr('(',')')
        self.G = graph
        self.idSet = set()

    def parse(self, input: str):
        clauses = set(input.split("&"))
        toParse = set()
        #clauses.split("=")
        for clause in clauses:
            leftSide = clause.split('=')[0]
            rightSide = clause.split('=')[1]
            leftSide = leftSide.strip()
            rightSide = rightSide.strip()
            toParse.add(leftSide)
            toParse.add(rightSide)
        
        final_set = []
        repeated_strings = set()

        for string in toParse:
            for other_string in toParse:
                if string != other_string and string in other_string:
                    repeated_strings.add(string)
                    break

        finalSetToParse = [string for string in toParse if string not in repeated_strings]

        for atom in finalSetToParse:
            atomAsList = self.myParser.parseString('(' + atom + ')').asList()
            parsedClause = self.parseClause(atomAsList[0])

        tmpG = self.G.copy()

        self.setCcpar()

        # Merge ccpar for duplicated nodes
        removed = set()
        for node in tmpG.nodes:
            for otherNode in tmpG.nodes:
                if otherNode in removed or node in removed:
                    continue
                firstNode = self.G.nodes[node]['node']
                secondNode = self.G.nodes[otherNode]['node']
                if firstNode == secondNode and firstNode.id != secondNode.id:
                    firstNode.ccpar = firstNode.ccpar.union(secondNode.ccpar)
                    for parent in secondNode.ccpar:
                        self.G.nodes[parent]['node'].args.remove(secondNode.id)
                        self.G.nodes[parent]['node'].args.append(firstNode.id)
                    self.G.remove_node(secondNode.id)
                    removed.add(secondNode.id)

        self.setEdges()

        return self.G
    
    def parseClause(self, clause: list) -> list:
        tmp = []

        # Correct the problem in parsing 
        for term in clause:
            if not(type(term) == list):
                for t in term.split(','):
                    if not(t == ''):
                        tmp.append(t)
            else:
                tmp.append(term)
        clause = tmp

        childrenNodes = []
        for i, literal in enumerate(clause):
            if type(literal) == list:
                continue
            if i + 1 < len(clause) and type(clause[i + 1]) == list:
                id = self.newId()
                args = self.parseClause(clause[i + 1])
                listIds = []
                for arg in args:
                    listIds.append(arg.id)
                newNode = Node(id=id, fn=literal, args=listIds, find=id)

            else:
                id = self.newId()
                newNode = Node(id=id, fn=literal, args=[], find=id)
            
            childrenNodes.append(newNode)
            self.G.add_node(newNode.id, node = newNode)

        return childrenNodes

    def setCcpar(self) -> None:
        for parent in self.G.nodes():
            children = self.G.nodes[parent]['node'].args
            for child in children:
                self.G.nodes[child]['node'].ccpar.add(parent)

    def setEdges(self) -> None:
        for parent in self.G.nodes():
            children = self.G.nodes[parent]['node'].args
            for child in children:
                self.G.add_edge(parent, child)

    def newId(self) -> str:
        id = 1

        while(True):
            if not(id in self.idSet):
                self.idSet.add(id)
                return id
            id += 1


def main():
    prsr = Parser(nx.DiGraph())
    clauses = "f(f(f(a)))=a & f(f(f(f(f(a)))))=a & f(a)=a "
    graph = prsr.parse(clauses)
    for node in graph.nodes():
        print(graph.nodes[node]['node'])
    print(graph.edges())
    

if __name__ == "__main__":
	main()	
