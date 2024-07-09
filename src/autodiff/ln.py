from functions import Function, Var, Val
from product import Product
from compose import Compose
from power import Inverse
import math


class _Ln(Function):

    def __init__(self) -> None:
        self.var = Var("dummy")
        super().__init__({self.var})
        

    def _evaluate(self, values: dict[Var, Val]) -> Val:
        if self.func(values) > 0:
            return Val(math.log(self.var(values)))
        else:
            raise ValueError("Ln undefined for x <= 0")
 
    
    def _partial(self, var:Var) -> Function:
        return Inverse(self.var)


class Ln(Compose):

    def __init__(self, func: Function) -> None:
        super().__init__(func, _Ln)
