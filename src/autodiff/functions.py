from __future__ import annotations
from autodiff.val import Val
from autodiff.var import Var

class Function():
    def __init__(self, vars: set[Var]) -> None:
        self.vars = vars


    def evaluate(self, values: dict[Var, Val]) -> Val:
        if values.keys != self.vars:
            raise ValueError("Wrong keys")
        self._evaluate(values)


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        raise NotImplementedError


    def differentiate(self, vars: set[Var]) -> Function:
        raise NotImplementedError
