from functions import Function, Var, Val
from product import Product
from neg import Neg
from compose import Compose
import math



class _Cos(Function):

    def __init__(self):
        self.var = Var("dummy")
        super().__init__({self.var})


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return Val(math.cos(self.var(values)))


    def differentiate(self, var: Var) -> Function:
        return Neg(Sin(self.var))


class Cos(Compose):

    def __init__(self, func: Function) -> None:
        super().__init__(func, _Cos())

        
class _Sin(Function):

    def __init__(self) -> None:
        self.var = Var("dummy")
        super().__init__({self.var})

        
    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return Val(math.sin(self.var(values)))

   
    def differentiate(self, var:Var) -> Function:
           return Cos(self.var)


class Sin(Compose):

    def __init__(self, func: Function) -> None:
        super().__init__(func, _Sin())
