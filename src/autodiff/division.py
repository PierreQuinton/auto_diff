from functions import Function, Product, Inverse


class Division(Product):

    def __init__(self, numerator: Function, denominator: Function) -> None:
        super().__init__(numerator, Inverse(denominator))
