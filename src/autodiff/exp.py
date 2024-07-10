from functions import Function, Var, Val
import math


class Exp(Function):
    
    def __init__(self, func: Function) -> None:
        self.func = func
        super.__init__([self.func])


    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        return Exp(self.func.substitute(substitutions))


    def _partial(self, func: Function) -> Function:
        return self
