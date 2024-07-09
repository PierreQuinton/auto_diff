from functions import Function, Var, Val
from product import Product
from neg import Neg
from compose import Compose
import math



class Cos(Function):

    def __init__(self, func: Function):
        self.func = func
        super().__init__({self.func})


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return Val(math.cos(self.func(values)))


    def _partial(self, func: Function) -> Function:
        return Neg(Sin(self.func))

        
class Sin(Function):

    def __init__(self, func: Function) -> None:
        self.func = func
        super().__init__({self.func})

        
    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return Val(math.sin(self.func(values)))

   
    def _partial(self, func: Function) -> Function:
           return Cos(self.func)
