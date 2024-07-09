from functions import Function, Var, Val
from product import Product, Neg
from sin import Sin
import math


class Cos(Function):

    def __init__(self, var:Var) -> None:
        self.var=var
        super().__init__({var})
        

    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return Val(math.cos(values[self.var]))

   
    def differentiate(self, var:Var) -> Function:
        return Product(Neg(Sin((self.var))), self.var.differentiate(var))
