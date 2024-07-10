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
        super().__init__({self})
    
    
    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return values[self]
    

    def differentiate(self, var: Var) -> Function:
        if self == var:
            return Val(1.0)
        else:
            return Val(0.0)


    def _partial(self, var: Var) -> Function:
        return Val(1.0)


class Val(Function):

    def __init__(self, val: float) -> None:
        self.val = val
        super().__init__(set())


    def __hash__(self) -> int:
            return self.val.__hash__()
    
    def __eq__(self, value: object) -> bool:
        if isinstance(self, value):
            return self.val == value.val
        return False


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return self


    def _partial(self, var: Var) -> Function:
        return Val(0.0)


def _flatten(functions: list[Function], type: Function) -> list[Function]:
    funcs = []
    for func in functions:
            if isinstance(func, type):
                funcs.update(func.functions)
            else:
                funcs.append(func)
    return funcs


class Sum(Function):

    def __init__(self, functions: list[Function]) -> None:
        self.func_list =_flatten(functions, Sum)
        super().__init__(set(self.func_list))


    def _evaluate(self, values:dict[Var, Val] ) -> Val:
        val = 0.0
        for function in self.func_list:
            val += function({var: values[var] for var in function.vars}).val
        return Val(val)

    
    def _partial(self, func: Function) -> Function:
        return Val(1.0)


class Product(Function):

    def __init__(self, functions: list[Function]):
        self.func_list =_flatten(functions, Product)
        super().__init__(set(self.func_list))


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        restricted_vals = [{var:values[var] for var in function.vars} for function in self.functions]
        fin_vals = [function(values).val for values, function in zip(restricted_vals, self.functions)]
        result = 1
        for i in fin_vals:
            result *= i
        return i


    def _partial(self, func: Function) -> Function:
        products = []
        count = 0
        for function in self.func_list:
            if function != func and not count:
                products.append(function)
            else:
                count = 1
        return Product(products)
