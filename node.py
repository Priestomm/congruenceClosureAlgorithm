class Node:

    def __init__(self, id: int, fn: str, args = [], find = None) -> None:
        self.id = id
        self.fn = fn
        self.args = args
        self.find = find
        self.ccpar = set()

    def __hash__(self):

        return hash(self.fn) * hash(tuple(self.args))

    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __repr__(self) -> str:
        return f" Node: \n\tid -> {self.id}\n\tfn -> {self.fn}\n\targs -> {self.args}\n\tfind -> {self.find}\n\tccpar -> {self.ccpar}\n"