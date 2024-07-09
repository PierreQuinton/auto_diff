from functions import Function, Var, Val
from product import Product
from compose import Compose
import math


class _Exp(Function):
    
    def __init__(self, var: Var) -> None:
        self.var = Var("dummy")
        super.__init__({var})


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return Val(math.exp(self.var(values)))


    def _partial(self, var: Var) -> Function:
        return self


class Exp(Compose):

    def __init__(self, func: Function) -> None:
        super().__init__(func, _Exp)
