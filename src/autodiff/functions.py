from __future__ import annotations


class Function():

    def __init__(self, funcs: set[Function]) -> None:
        self.funcs = funcs
        self.vars = {var for function in funcs for var in function.funcs}


    def __apply__(self, values: dict[Var, Val]) -> Val:
        if values.keys != self.funcs:
            raise ValueError("Wrong keys")
        self._evaluate(values)


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        """
        This raises an error when the program didn't find 
         an evalutation in the already implemented functions.
        """
        raise NotImplementedError

    def partial(self, func: Function) -> Function:
        if func not in self.funcs:
            raise ValueError("Cannot take partial derivative wrt independent function")
        return self._partial(func)

    def _partial(self, func: Function) -> Function:
        """
        This raises an error when the program didn't find 
         an differentiation in the already implemented functions.
        """
        raise NotImplementedError
    
    def differentiate(self, var: Var) -> Function:
        return Sum([
            Product([self.partial(func), func.differentiate(var)])
            for func in self.funcs
        ])

class Var(Function):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(set(self))
    
    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return values[self]
    
    def _partial(self, var: Var) -> Function:
        if var in self.funcs:
            return Val(1.0)
        else:
            return Val(0.0)


class Val(Function):

    def __init__(self, val: float) -> None:
        self.val = val
        super().__init__(set())
    
    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return self


    def _partial(self, var: Var) -> Function:
        return Val(0.0)


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
