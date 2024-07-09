from functions import Function
from product import Product
from val import Val
from var import Var
import math


class Ln(Function):

    def __init__(self, var:Var) -> None:
        self.var=var
        super().__init__({var})
        

    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return Val(math.log(values[self.var]))
 
    
    def differentiate(self, var:Var) -> Function:
        raise NotImplementedError
