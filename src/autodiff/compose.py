from autodiff.functions import Function
from autodiff.product import Product
from autodiff.val import Val
from autodiff.var import Var

class Compose(Function):
    def __init__(self, inner: Function, outer: Function) -> None:
        self.inner = inner
        self.outer = outer
        super().__init__(inner.vars)

        if len(self.outer.vars) != 1:
            raise ValueError("Expected only one argument")
        
        self.outer_var = list(self.outer.vars)[0]


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        inner_val = self.inner.evaluate(values)
        return self.outer.evaluate({self.outer_var: inner_val})


    def differentiate(self, var: Var) -> Function:
        return Product([self.inner.differentiate(var), Compose(self.outer.differentiate(var), self.inner)])
    