from functions import Function, Var, Val
from product import Product


class Compose(Function):

    def __init__(self, inner: Function, outer: Function) -> None:
        self.inner = inner
        self.outer = outer
        super().__init__(inner.funcs)

        if len(self.outer.funcs) != 1:
            raise ValueError("Expected only one argument")
        
        self.outer_var = list(self.outer.funcs)[0]


    def _evaluate(self, values: dict[Var, Val]) -> Val:
        inner_val = self.inner(values)
        return self.outer({self.outer_var: inner_val})


    def _partial(self, var: Var) -> Function:
        return Product([self.inner._partial(var), Compose(self.outer._partial(var), self.inner)])
    