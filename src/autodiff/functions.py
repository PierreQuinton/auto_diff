from __future__ import annotations


class Function():

    def __init__(self, vars: set[Var]) -> None:
        self.vars = vars


    def __apply__(self, values: dict[Var, Val]) -> Val:
        if values.keys != self.vars:
            raise ValueError("Wrong keys")
        self._evaluate(values)


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        raise NotImplementedError


    def differentiate(self, var: Var) -> Function:
        raise NotImplementedError


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


class Val(Function):

    def __init__(self, val: float) -> None:
        self.val = val
        super().__init__(set())
    
    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return self


    def differentiate(self, var: Var) -> Function:
        return Val(0.0)
