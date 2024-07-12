from autodiff import *


def gradient_descent(function: Function, xs_0: dict[Var, float], learning_rate: float, max_iter: int = 100, norm_epsilon: float = 1e-04) -> dict[Var, float]:
    xs = xs_0
    grad = function.differentiate(set(xs.keys()))
    for i in range(max_iter):
        norm = 0.0
        new_xs = {}
        for x, x_val in xs.items():
            x_update = grad[x].evaluate(xs)
            norm += x_update**2
            new_xs[x] = x_val - learning_rate * x_update
        norm **= 1/2
        xs = new_xs
        if norm < norm_epsilon:
            break
    return xs
