from __future__ import annotations
from autodiff.functions import Function
from autodiff.var import Var

class Val(Function):
    def __init__(self, val: float) -> None:
        self.val = val
        super().__init__(set())
    
    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return self


    def differentiate(self, vars: set[Var]) -> Function:
        return Val(0.0)
