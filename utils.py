import matplotlib.pyplot as plt

def plot_values(x_values, y_values):
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(x_values, y_values)  # Plot some data on the axes
    plt.show(block=False)

def hold_execution():
    plt.show(block=True)