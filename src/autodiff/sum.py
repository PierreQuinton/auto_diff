from autodiff.functions import Function
from autodiff.val import Val
from autodiff.var import Var


class Sum(Function):
    def __init__(self, functions: list[Function]) -> None:
        self.functions = functions

        super().__init__({var for function in functions for var in function.vars})

    def evaluate(self, values:dict[Var, Val] ) -> Val:
        val=0.0
        for function in self.functions:
            val+=function.evaluate({var: values[var] for var in function.vars}).val
        return Val(val)


   
    def differentiate(self, var:Var) -> Function:
        list_derivatives=[]
        for function in self.functions :
            list_derivatives.append(function.differentiate(var))
           
        return Sum(list_derivatives)
