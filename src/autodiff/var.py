from __future__ import annotations
from autodiff.functions import Function
from autodiff.val import Val

class Var(Function):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(set(self))
    
    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return values[self]
    
    # def differentiate(self, var: Var) -> Function:
    #     return Val(0 , 1)
    