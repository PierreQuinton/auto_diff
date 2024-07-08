from autodiff.functions import Function
from autodiff.val import Val
from autodiff.var import Var
import math
from autodiff.cos import Cos


class Sin(Function):
    def __init__(self, var:Var) -> None:
        self.var=var
        super().__init__({var})
        

    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return Val(math.sin(values[self.var]))

   
    def differentiate(self, var:Var) -> Function:
           if var==self.var:
                return Cos(var)
           else:
                return Val(0.0)
