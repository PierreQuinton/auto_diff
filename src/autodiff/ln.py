from functions import Function, Var, Val
from power import Inverse
import math


class Ln(Function):

    def __init__(self, func: Function) -> None:
        self.func = func
        super().__init__({self.func})
        

    def _evaluate(self, values: dict[Var, Val]) -> Val:
        if self.func(values) > 0:
            return Val(math.log(self.func(values)))
        else:
            raise ValueError("Ln undefined for x <= 0")
 
    
    def _partial(self, func: Function) -> Function:
        return Inverse(self.func)
