from functions import Function, Var, Val
from product import Product


class Power(Function):
    def __init__(self, base: Function, exp: Function) -> None:
        self.base = base
        self.exp = exp
        super().__init__(base.vars|exp.vars)

    def _evaluate(self, values: dict[Var, Val]) -> Val:
        exp_val = self.exp({var:values[var] for var in self.exp.vars})
        base_val = self.base({var:values[var] for var in self.base.vars})
        return Val(base_val.val ** exp_val.val)

    def differentiate(self, var: Var) -> Function:
        if isinstance(self.exp, Val):
            return Product([self.exp, self.base.differentiate(var), Power(self.base, Val(self.exp.val-1))])
        else:
            raise NotImplementedError("Power rule not implemented for non-constant exponents")


class Inverse(Power):

    def __init__(self, function: Function) -> None:
        super().__init__(function, Val(-1.0))
