from functions import Function, Product
from power import Inverse


class Division(Product):

    def __init__(self, numerator: Function, denominator: Function) -> None:
        super().__init__(numerator, Inverse(denominator))


    def __repr__(self):
        string = """This class handles division and division differentiation"""
