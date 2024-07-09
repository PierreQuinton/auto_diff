from functions import Function, Var, Val


class Sum(Function):
    def __init__(self, functions: list[Function]) -> None:
        funcs = []

        for func in functions:
            if isinstance(func, Sum):
                funcs.update(func.functions)
            else:
                funcs.append(func)

        super().__init__(funcs)


    def __apply__(self, values:dict[Var, Val] ) -> Val:
        val = 0.0
        for function in self.functions:
            val += function({var: values[var] for var in function.vars}).val
        return Val(val)

    
    def _partial(self, func: Function) -> Function:
        return Val(1.0)
