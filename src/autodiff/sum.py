from functions import Function, Var, Val


class Sum(Function):
    def __init__(self, functions: list[Function]) -> None:
        self.functions = functions

        super().__init__({var for function in functions for var in function.vars})

    def __apply__(self, values:dict[Var, Val] ) -> Val:
        val=0.0
        for function in self.functions:
            val+=function({var: values[var] for var in function.vars}).val
        return Val(val)

   
    def differentiate(self, var:Var) -> Function:
        list_derivatives=[]
        for function in self.functions :
            list_derivatives.append(function.differentiate(var))
           
        return Sum(list_derivatives)
