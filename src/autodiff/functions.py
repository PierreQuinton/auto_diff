from __future__ import annotations
from collections import Counter
from typing import Iterable, cast
import math


class Function:

    def __init__(self, funcs: Iterable[Function]) -> None:
        self.funcs = tuple(funcs)

    # def __apply__(self, values: dict[Var, Val]) -> Val:
    #     if values.keys != self.funcs:
    #         raise ValueError("Wrong keys")
    #     self._substitute(values)
    def evaluate(self, substitutions: dict[Var, float]) -> float:
        final_val = self.substitute({var: Val(val) for var, val in substitutions.items()})._simplify()
        if isinstance(final_val, Val):
            return final_val.val
        raise ValueError("Should provide substitution for all Vars")

    def simplify(self) -> Function:
        return _SimplifiedFunction(self._simplify())

    def _simplify(self) -> Function:
        raise NotImplementedError

    def substitute(self, substitutions: dict[Function, Function]) -> Function:
        if self in substitutions:
            return substitutions[self]
        return self._substitute(substitutions)

    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        raise NotImplementedError

    def partial(self, func: Function) -> Function:
        if func not in self.funcs:
            raise ValueError("Cannot take partial derivative wrt independent function")
        return self._partial(func)

    def _partial(self, func: Function) -> Function:
        """
        This raises an error when the program didn't find a differentiation in the already implemented functions.
        """
        raise NotImplementedError

    def _list_representation(self) -> tuple[str | Function, ...]:
        return self.__class__.__name__, *self.funcs

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Function):
            return self._list_representation() == other._list_representation()
        return False

    def __hash__(self) -> int:
        return self._list_representation().__hash__()

    def differentiate(self, variables: set[Var]) -> dict[Var, Function]:
        gradient = {}

        for var in variables:
            simplified_self = self._simplify()
            gradient[var] = simplified_self._differentiate(var)._simplify()
        return gradient
    
    def _differentiate(self, var: Var) -> Function:
        return Sum([
            Product([self.partial(func), func._differentiate(var)])
            for func in self.funcs
        ])

    def __add__(self, other: Function | float | int):
        if isinstance(other, Function):
            return Sum([self, other])
        elif isinstance(other, float):
            return Sum([self, Val(other)])
        elif isinstance(other, int):
            return Sum([self, Val(float(other))])

    __radd__ = __add__

    def __sub__(self, other: Function | float | int):
        if isinstance(other, Function):
            return Subtraction(self, other)
        elif isinstance(other, float):
            return Subtraction(self, Val(other))
        elif isinstance(other, int):
            return Subtraction(self, Val(float(other)))

    def __mul__(self, other: Function | float | int):
        if isinstance(other, Function):
            return Product([self, other])
        elif isinstance(other, float):
            return Product([self, Val(other)])
        elif isinstance(other, int):
            return Product([self, Val(float(other))])

    __rmul__ = __mul__

    def __truediv__(self, other: Function | float | int):
        if isinstance(other, Function):
            return Division(self, other)
        elif isinstance(other, float):
            return Division(self, Val(other))
        elif isinstance(other, int):
            return Division(self, Val(float(other)))

    def __pow__(self, other: Function | float | int):
        if isinstance(other, Function):
            return Power(self, other)
        elif isinstance(other, float):
            return Power(self, Val(other))
        elif isinstance(other, int):
            return IntegerPower(self, other)
    
    def __repr__(self) -> str:
        return self.__str__()


class _SimplifiedFunction(Function):
    def __init__(self, func: Function):
        super().__init__([func])
        self.func = func

    def simplify(self) -> Function:
        return self

    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        return self.func._substitute(substitutions)

    def _partial(self, func: Function) -> Function:
        return self.func._partial(func)


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

    def _differentiate(self, var: Var) -> Function:
        if self == var:
            return Val(1.0)
        else:
            return Val(0.0)

    def _partial(self, var: Var) -> Function:
        return Val(1.0)

    def __str__(self) -> str:
        return str(self.name)

    def _simplify(self) -> Function:
        return self


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

    def _simplify(self) -> Function:
        return self


def _flatten(functions: Iterable[Function], t: type[Sum] | type[Product]) -> Counter[Function]:
    funcs = Counter()
    for func in functions:
        if isinstance(func, t):
            funcs.update(func.funcs)
        else:
            funcs.update([func])
    return funcs


class Sum(Function):

    def __init__(self, functions: Iterable[Function]) -> None:
        self.func_counter = _flatten(functions, Sum)
        self.funcs = list(self.func_counter.elements())
        super().__init__(self.funcs)

    def __hash__(self) -> int:
        return 2 * tuple(self.func_counter.elements()).__hash__()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Sum):
            return self.func_counter == other.func_counter
        return False

    def _simplify(self) -> Function:
        funcs = []
        for func in self.func_counter:
            funcs += [func._simplify()] * self.func_counter[func]
        monomials = dict()
        for func in funcs:
            # print(func.__class__)
            if isinstance(func, Neg) and func != self.funcs[0]:
                print(func, self.funcs[0])
                func = Subtraction(self, func)

            if isinstance(func, Val):
                terms = tuple()
                val = func.val

            else:
                if not isinstance(func, Product):
                    terms = (func,)
                    val = 1.0
                elif isinstance(func.funcs[0], Val):
                    terms = tuple(func.funcs[1:])
                    val = cast(Val, func.funcs[0]).val
                else:
                    terms = tuple(func.funcs)
                    val = 1.0
            if terms in monomials:
                monomials[terms] += val
            else:
                monomials[terms] = val

        funcs = [Product([Val(val), *terms])._simplify() for terms, val in monomials.items()]
        funcs = [func for func in funcs if func != Val(0.0)]

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
        return "+".join([func.__str__() for func in self.funcs])


class Subtraction(Sum):

    def __init__(self, function_1: Function, function_2: Function) -> None:
        super().__init__([function_1, Neg(function_2)])


class Product(Function):

    def __init__(self, functions: Iterable[Function]):
        self.func_counter = _flatten(functions, Product)
        super().__init__(list(self.func_counter.elements()))

    def __hash__(self) -> int:
        return 3 * tuple(self.func_counter.elements()).__hash__()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Product):
            return self.func_counter == other.func_counter
        return False

    def _simplify(self) -> Function:
        funcs = []
        for func in self.func_counter:
            funcs += [func._simplify()] * self.func_counter[func]
        val = 1.0
        non_val_funcs = []
        for func in funcs:
            if isinstance(func, Val):
                if func.val == 0.0:
                    return Val(0.0)
                val *= func.val
            else:
                non_val_funcs += [func]

        if val == 1.0:
            funcs = non_val_funcs
        else:
            funcs = [Val(val), *non_val_funcs]

        if len(funcs) == 0:
            return Val(1.0)
        elif len(funcs) == 1:
            return funcs[0]
        return Product(funcs)

    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        funcs = []
        for func in self.func_counter:
            funcs += [func.substitute(substitutions)] * self.func_counter[func]
        return Product(funcs)

    def _partial(self, func: Function) -> Function:
        products = []
        for function, count in self.func_counter.items():
            if function == func:
                products.append(IntegerPower(function, count-1))
            else:
                products.append(IntegerPower(function, count))
        return Product(products)

    def __str__(self) -> str:
        return "(" + ")⋅(".join([f.__str__() for f in self.funcs]) + ")"


class Division(Product):

    def __init__(self, numerator: Function, denominator: Function) -> None:
        self.numerator = numerator
        self.denominator = denominator
        super().__init__([numerator, Inverse(denominator)])

    def __str__(self) -> str:
        return "(" + self.numerator.__str__() + ")" + "/" + "(" + self.denominator.__str__() + ")"

    def _simplify(self) -> Function:
        denominator = self.denominator._simplify()
        numerator = self.numerator._simplify()
        if denominator == Val(1.0):
            return numerator
        elif numerator == Val(1.0):
            return Inverse(denominator)
        return Division(denominator, numerator)


class Neg(Product):

    def __init__(self, function: Function):
        super().__init__([Val(-1), function])
        self.function = function

    # def __str__(self) -> str:
    #     return "-" + self.function.__str__()


class Exp(Function):

    def __init__(self, func: Function) -> None:
        self.func = func
        super().__init__([self.func])

    def _simplify(self) -> Function:
        func = self.func._simplify()
        if isinstance(func, Val):
            return Val(math.exp(func.val))
        elif isinstance(func, Ln):
            return func.func
        return Exp(func)

    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        return Exp(self.func.substitute(substitutions))

    def _partial(self, func: Function) -> Function:
        return self

    def __str__(self) -> str:
        return "exp(" + self.func.__str__() + ")"


class IntegerPower(Function):

    def __init__(self, base: Function, exp: int) -> None:
        self.exp = exp
        self.base = base
        super().__init__([base])

    def _simplify(self) -> Function:
        base = self.base._simplify()
        if isinstance(base, Val):
            return Val(base.val ** self.exp)
        elif self.exp == 0:
            return Val(1.0)
        elif self.exp == 1:
            return base
        return IntegerPower(base, self.exp)

    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        return IntegerPower(self.base.substitute(substitutions), self.exp)

    def _partial(self, func: Function) -> Function:
        return Product([Val(float(self.exp)), IntegerPower(self.base, self.exp - 1)])

    def __str__(self) -> str:
        if self.exp < 0.0:
            exp = "(" + str(self.exp) + ")"
        else:
            exp = str(self.exp)
        return "(" + str(self.base) + ")" + "^" + str(exp)


class Power(Exp):

    def __init__(self, base: Function, exp: Function) -> None:
        self.base = base
        self.exp = exp
        func = Product([Ln(base), exp])
        super().__init__(func)

    def __str__(self) -> str:
        return "(" + self.base.__str__() + ")" + "^" + "(" + self.exp.__str__() + ")"


class Inverse(IntegerPower):

    def __init__(self, function: Function) -> None:
        super().__init__(function, -1)


class Ln(Function):

    def __init__(self, func: Function) -> None:
        self.func = func
        super().__init__([self.func])

    def _simplify(self) -> Function:
        func = self.func._simplify()
        if isinstance(func, Val):
            return Val(math.log(func.val))
        elif isinstance(func, Exp):
            return func.func
        return Ln(func)

    def _substitute(self, substitutions: dict[Function, Function]) -> Function:
        return Ln(self.func.substitute(substitutions))

    def _partial(self, func: Function) -> Function:
        return Inverse(self.func)

    def __str__(self) -> str:
        return "log(" + self.func.__str__() + ")"
