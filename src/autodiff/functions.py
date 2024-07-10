from __future__ import annotations
from collections import Counter

from typing import Iterable, cast


class Function():

    def __init__(self, funcs: list[Function]) -> None:
        self.funcs = funcs


    # def __apply__(self, values: dict[Var, Val]) -> Val:
    #     if values.keys != self.funcs:
    #         raise ValueError("Wrong keys")
    #     self._substitute(values)


    def simplify(self) -> Function:
        raise NotImplementedError


    def substitute(self, substitutions: dict[Function, Function]) -> Function:
        if self in substitutions:
            return substitutions[self]
        return self._substitute(substitutions)


    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        raise NotImplementedError


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
    

    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        return self


    def differentiate(self, var: Var) -> Function:
        if self == var:
            return Val(1.0)
        else:
            return Val(0.0)


    def _partial(self, var: Var) -> Function:
        return Val(1.0)
    

    def __str__(self) -> str:
        return str(self.name)


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


    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        return self


    def _partial(self, var: Var) -> Function:
        return Val(0.0)
    

    def __str__(self) -> str:
        return str(self.val)


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
        self.func_list = list(self.func_counter.elements())
        super().__init__(self.func_list)


    def __hash__(self) -> int:
        return self.func_counter.__hash__()


    def __eq__(self, other: object) -> bool:
        if isinstance(other, Sum):
            return self.func_counter == other.func_counter
        return False


    def simplify(self) -> Function:
        funcs = []
        for func in self.func_counter:
            funcs += [func.simplify()] * self.func_counter[func]
        non_val_funcs = []
        func_dict = dict()
        for func in funcs:
            if isinstance(func, Val):
                term = Product([])
                val = func.val
            else:
                if not isinstance(func, Product):
                    term = Product([func])
                    val = 1.0
                elif not isinstance(func.funcs[0], Val):
                    term = Product(func.funcs)
                    val = 1.0
                else:
                    term = Product(func.funcs[1:])
                    val = func.funcs[0].val
            if term in func_dict:
                func_dict[term] += val
            else:
                func_dict[term] = val

        funcs = [Product([Val(val), *cast(Product, term).funcs]).simplify() for term, val in func_dict.items()]

        if len(funcs) == 0:
            return Val(0.0)
        if len(funcs) == 1:
            return funcs[0]
        return Sum(funcs)

    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        funcs = []
        for func in self.func_counter:
            funcs += [func.substitute(substitutions)] * self.func_counter[func]
        return Sum(funcs)
    
    def _partial(self, func: Function) -> Function:
        return Val(1.0)


    def __str__(self) -> str:
        return "+".join(self.func_list)  # Is it func_list?


class Product(Function):

    def __init__(self, functions: Iterable[Function]):
        self.func_counter =_flatten(functions, Product)
        self.func_list = list(self.func_counter.elements())
        super().__init__(self.func_list)


    def __hash__(self) -> int:
        return self.func_counter.__hash__()


    def __eq__(self, other: object) -> bool:
        if isinstance(other, Product):
            return self.func_counter == other.func_counter
        return False


    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        funcs = []
        for func in self.func_counter:
            funcs += [func.substitute(substitutions)] * self.func_counter[func]
        return Product(funcs)


    def _partial(self, func: Function) -> Function:
        products = []
        count = 0
        for function in self.func_counter:
            if function != func and not count:
                products.append(function)
            else:
                count = 1
        return Product(products)
    

    def __str__(self) -> str:
        return " ".join([f.__str__() for f in self.func_list])  # Is it func_list?


class Exp(Function):
    
    def __init__(self, func: Function) -> None:
        self.func = func
        super.__init__([self.func])


    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        return Exp(self.func.substitute(substitutions))


    def _partial(self, func: Function) -> Function:
        return self
    

    def __str__(self) -> str:
        return "exp("+ self.func.__str__() +")"


class Power(Exp):

    def __init__(self, base: Function, exp: Function) -> None:
        func = Product(Ln(base), exp)
        super().__init__(func)


class Inverse(Power):

    def __init__(self, function: Function) -> None:
        super().__init__(function, Val(-1.0))


class Ln(Function):

    def __init__(self, func: Function) -> None:
        self.func = func
        super().__init__([self.func])
         
    
    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        return Ln(self.func.substitute(substitutions))
    
    
    def _partial(self, func: Function) -> Function:
        return Inverse(self.func)


    def __str__(self) -> str:
        return "log(" + self.func.__str__ + ")"