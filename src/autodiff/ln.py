from autodiff.functions import Function
from autodiff.product import Product
import math
from autodiff.val import Val
from autodiff.var import Var

class Ln(Function):
    def __init__(self, var:Var) -> None:
        self.var=var
        super().__init__({var})
        

    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return Val(math.log(values[self.var]))
 
    
    def differentiate(self, var:Var) -> Function:
        raise NotImplementedError