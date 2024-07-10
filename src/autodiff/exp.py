from functions import Function, Var, Val
import math


class Exp(Function):
    
    def __init__(self, func: Function) -> None:
        self.func = func
        super.__init__([self.func])


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return Val(math.exp(self.func(values)))


    def _partial(self, func: Function) -> Function:
        return self
