from autodiff import *
from matplotlib import pyplot as plt


def plot_graph(where, points_x, points_y, style="b-", title="Graph", x_label="x", y_label="y"):
    where.plot(points_x, points_y, style)
    where.set_title(title)
    where.set_xlabel(x_label)
    where.set_ylabel(y_label)


def plot_one_var_function(func: Function, var: Var, grad_dict_list: list[dict[Var, float]], n_points: int = 365, learning_rate=""):
    fig, axis = plt.subplots()
    y_vals = []
    if not isinstance(var, Var):
        raise ValueError("Function must be a function of one variable")
    grad_list_x = [x for d in grad_dict_list for x in d.values()]
    grad_list_y = [func.evaluate(x) for x in grad_dict_list]
    x_range = (min(grad_list_x), max(grad_list_x))
    x_points = [x_range[0] + i * (x_range[1] - x_range[0]) / n_points for i in range(n_points)]
    for x in x_points:
        y_vals.append(func.evaluate({var: x}))
    plot_graph(axis, x_points, y_vals, "b-")
    plot_graph(axis, grad_list_x, grad_list_y, "rx", title="Graph - "+str(learning_rate))
    plt.show()
