from __future__ import annotations
from collections import Counter

from typing import Iterable


class Function():

    def __init__(self, funcs: list[Function]) -> None:
        self.funcs = funcs


    def __apply__(self, values: dict[Var, Val]) -> Val:
        if values.keys != self.funcs:
            raise ValueError("Wrong keys")
        self._evaluate(values)


    def substitute(self, substitutions: dict[Function, Function]) -> Function:
        if self in substitutions:
            return substitutions[self]
        return self._substitute(substitutions)


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
    

    def _list_representation(self) -> list[type | Function]:
        return [self.__class__] + self.funcs
    

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Function):
            return self._list_representation() == other._list_representation()
        return False
    

    def __hash__(self) -> int:
        return self._list_representation().__hash__()

    
    def differentiate(self, var: Var) -> Function:
        return Sum([
            Product([self.partial(func), func.differentiate(var)])
            for func in self.funcs
        ])


class Var(Function):
    
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__({self})
        
    def __hash__(self) -> int:
        return self.name.__hash__()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Var):
            return self.name == other.name
        return False
    
    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return values[self]
    

    def substitute(self, substitutions: dict[Function, Function]) -> Function:
        return substitutions[self]
    

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


    def __eq__(self, other: object) -> bool:
        if isinstance(other, Val):
            return self.val == other.val
        return False


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        return self


    def _partial(self, var: Var) -> Function:
        return Val(0.0)


def _flatten(functions: list[Function], type: Function) -> Counter[Function]:
    funcs = Counter()
    for func in functions:
            if isinstance(func, type):
                funcs.update(func.func_counter)
            else:
                funcs.update([func])
    return funcs


class Sum(Function):

    def __init__(self, functions: Iterable[Function]) -> None:
        self.func_counter =_flatten(functions, Sum)
        super().__init__(list(self.func_counter.elements()))


    def __hash__(self) -> int:
        return self.func_counter.__hash__()


    def __eq__(self, other: object) -> bool:
        if isinstance(other, Sum):
            return self.func_counter == other.func_counter
        return False


    def _evaluate(self, values:dict[Var, Val] ) -> Val:
        val = 0.0
        for function in self.func_counter:
            val += function({var: values[var] for var in function.vars}).val
        return Val(val)

    
    def _partial(self, func: Function) -> Function:
        return Val(1.0)


class Product(Function):

    def __init__(self, functions: Iterable[Function]):
        self.func_counter =_flatten(functions, Product)
        super().__init__(list(self.func_counter))


    def __hash__(self) -> int:
        return self.func_counter.__hash__()


    def __eq__(self, other: object) -> bool:
        if isinstance(other, Product):
            return self.func_counter == other.func_counter
        return False


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
        for function in self.func_counter:
            if function != func and not count:
                products.append(function)
            else:
                count = 1
        return Product(products)
