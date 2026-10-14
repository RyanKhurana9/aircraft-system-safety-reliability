from functools import reduce
from operator import and_, or_

class Node:
    def events(self) -> list[str]: raise NotImplementedError
    def prob(self, q: dict) -> float: raise NotImplementedError
    def failed(self, state: dict):
        """state[name] = bool or numpy bool array (True = component failed)."""
        raise NotImplementedError

    def validate(self):
        ev = self.events()
        dup = {e for e in ev if ev.count(e) > 1}
        if dup:
            raise ValueError(f"Repeated basic events {dup}: independence "
                             "assumption invalid; use cut sets instead.")

class Basic(Node):
    def __init__(self, name): self.name = name
    def events(self): return [self.name]
    def prob(self, q): return q[self.name]
    def failed(self, state): return state[self.name]

class Gate(Node):
    def __init__(self, *children): self.children = children
    def events(self): return [e for c in self.children for e in c.events()]

class AND(Gate):
    def prob(self, q):
        p = 1.0
        for c in self.children: p *= c.prob(q)
        return p
    def failed(self, state): return reduce(and_, (c.failed(state) for c in self.children))

class OR(Gate):
    def prob(self, q):
        p = 1.0
        for c in self.children: p *= 1 - c.prob(q)
        return 1 - p
    def failed(self, state): return reduce(or_, (c.failed(state) for c in self.children))