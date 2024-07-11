from functions import Function, Product, Inverse


class Division(Product):

    def __init__(self, numerator: Function, denominator: Function) -> None:
        self.nu
        super().__init__(numerator, Inverse(denominator))


    def __str__(self) -> str:
        return 