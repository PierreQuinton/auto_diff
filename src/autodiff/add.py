from autodiff.functions import Function
from autodiff.val import Val
from autodiff.var import Var


class Add(Function):
    def __init__(self, functions: list[Function]) -> None:
        self.functions = functions

        super().__init__({var for function in functions for var in function.vars})

    def evaluate(self, values:dict[Var, Val] ) -> Val:
        val=0.0
        for function in self.functions:
            val+=function.evaluate({var: values[var] for var in function.vars}).val
        return Val(val)


   
    def differentiate(self, var:Var) -> Function:
        raise NotImplementedError
        # Multiply([self.innner.differentiate(), Compose(self.outer.differentiate, self.inner)