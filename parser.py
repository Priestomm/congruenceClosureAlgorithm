from pyparsing import nestedExpr
from node import Node
import networkx as nx
import matplotlib.pyplot as plt

class Parser:

    def __init__(self, graph = None) -> None:
        self.myParser = nestedExpr('(',')')
        self.G = graph
        self.idSet = set()

    def parse(self, input: str):
        input = input.split("&")
        clauses = set(i[1:-1] for i in input)
        toParse = set()
        #clauses.split("=")
        for clause in clauses:
            clause = clause.replace("!","")
            if clause[0] == '(':
                clause = clause[1:-1]
            leftSide = clause.split('=')[0]
            rightSide = clause.split('=')[1]
            toParse.add(leftSide)
            toParse.add(rightSide)
        
        final_set = []
        repeated_strings = set()

        for string in toParse:
            for other_string in toParse:
                if string != other_string and string in other_string and other_string[other_string.find(string)+len(string)] in ['=','(',')']:
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
                        self.G.nodes[parent]['node'].args[self.G.nodes[parent]['node'].args.index(secondNode.id)] = firstNode.id
                    self.G.remove_node(secondNode.id)
                    removed.add(secondNode.id)

        self.setEdges()

    
    def splitEq(self, clauses: str):
        equalSet = set()
        nonEqualSet = set()
        clauses = clauses.split("&")
        clauses = set(i.strip()[1:-1] for i in clauses)
        for clause in clauses:
            if "!" in clause:
                clause = clause.replace('!','')
                if clause[0] == '(':
                    clause = clause[1:-1]
                sides = clause.split("=")
                nonEqualSet.add((sides[0], sides[1]))
            else:
                sides = clause.split("=")
                equalSet.add((sides[0], sides[1]))

        return equalSet, nonEqualSet
    
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
    
    def subtermsSet(self) -> set():
        retSet = set()
        for node in self.G.nodes():
            retSet.add((self.stringFromNode(self.G.nodes[node]['node']), node))
        return retSet

    def stringFromNode(self, node: Node):
        retString = ""
        retString += node.fn

        if len(node.args) > 0:
            retString += "("
            for i, arg in enumerate(node.args):
                retString += self.stringFromNode(self.G.nodes[arg]['node'])
                if i + 1 < len(node.args):
                    retString += ","
            retString += ")"
        return retString
        
    def nodeFromString(self, stringNode: str):

        for pair in self.subtermsSet():
            node, id = pair
            if stringNode == node:
                return self.G.nodes[id]['node']

    def newId(self) -> str:
        id = 1

        while(True):
            if not(id in self.idSet):
                self.idSet.add(id)
                return id
            id += 1

