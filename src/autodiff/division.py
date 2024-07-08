from autodiff.functions import Function
from autodiff.sum import Sum
from __future__ import annotations
from autodiff.compose import Compose
from autodiff.val import Val
from autodiff.var import Var


class Division(Function):

    def __init__(self, numerator: Function, denominator: Function):
        self.numerator = numerator
        self.denominator = denominator
        super().__init__()


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        restricted_vals = [{var:values[var] for var in function.vars} for function in self.functions]
        fin_vals = [function.evaluate(values).val for values, function in zip(restricted_vals, self.functions)]
        result = self.numerator/self.denominator


    def differentiate(self, var: Var) -> Function:
        functions= function.differentiate
        products = []
        for i, function in enumerate(self.functions):
            functions = self.functions[:i] + [function.differentiate(var)] + self.functions[i+1:]
            products.append(Product(functions))

        return Sum(products)

