from matplotlib import pyplot as plt

def plot_graph(points):
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    plt.plot(x, y)
    plt.show()

plot_graph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)])
