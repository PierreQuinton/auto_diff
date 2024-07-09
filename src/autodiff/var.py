from __future__ import annotations
from functions import Function
from val import Val

class Var(Function):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(set(self))
    
    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return values[self]
    
    def differentiate(self, var: Var) -> Function:
        if var in self.vars:
            return Val(1.0)
        else:
            return Val(0.0)
