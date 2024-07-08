from autodiff.functions import Function
from autodiff.sum import Sum
from __future__ import annotations
from autodiff.compose import Compose
from autodiff.val import Val
from autodiff.var import Var


class Product(Function):

    def __init__(self, functions: set[Function]):
        super().__init__({var for function in functions for var in function.vars})
        self.functions = functions


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        restricted_vals = [{var:values[var] for var in function.vars} for function in self.functions]
        fin_vals = [function.evaluate(values).val for values, function in zip(restricted_vals, self.functions)]
        result = 1
        for i in fin_vals:
            result *= i
        return i


    def differentiate(self, var: Var) -> Function:
        products = []
        for i, function in enumerate(self.functions):
            functions = self.functions[:i] + [function.differentiate(var)] + self.functions[i+1:]
            products.append(Product(functions))

        return Sum(products)


class Neg(Product):

    def __init__(self, function: Function):
        super().__init__([Val(-1), function])
