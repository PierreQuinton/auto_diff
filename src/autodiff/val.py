from autodiff.expr import Expr

class Val(Expr):
    def __init__(self, val: float) -> None:
        self.val = val
