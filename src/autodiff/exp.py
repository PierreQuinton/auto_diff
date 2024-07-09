from functions import Function, Var, Val
from product import Product
import math

class Exp(Function):
    
    def __init__(self, var: Var) -> None:
        self.var = var
        super.__init__({var})


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return Val(math.exp(values[self.var]))
    

    def differentiate(self, var: Var) -> Function:
        return Product(self, self.var.differentiate(var))
