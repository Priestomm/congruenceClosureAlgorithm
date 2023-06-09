import re

clauses = ["f(g(a,b),b) = g(c)", "g(x) = f(a, b)", "h(g(y)) = z"]

# Extract subterms from each clause
subterms = set()

def parse(part: str):
    currentSymbol = ""
    for i, char in enumerate(part):
        if char == ",":
            subterms.add(currentSymbol)
        if char == "(":
            subterms.add(currentSymbol + part[i:len(part)])
            parse(part[i + 1:len(part) - 1])
            break
        currentSymbol += char

for clause in clauses:
    clause = clause.replace(" ", "")
    parts = clause.split("=")
    for part in parts:
        parse(part)


            

