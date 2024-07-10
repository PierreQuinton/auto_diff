from functions import Function, Product
from power_ln_inverse import Inverse


class Division(Product):

    def __init__(self, numerator: Function, denominator: Function) -> None:
        super().__init__(numerator, Inverse(denominator))

