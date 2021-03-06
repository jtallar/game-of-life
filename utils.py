import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Formatter taken from 
# https://stackoverflow.com/questions/25750170/show-decimal-places-and-scientific-notation-on-the-axis-of-a-matplotlib-plot
class MathTextSciFormatter(mticker.Formatter):
    def __init__(self, fmt="%1.2e"):
        self.fmt = fmt

    def __call__(self, x, pos=None):
        s = self.fmt % x
        dec_point = '.'
        pos_sign = '+'
        tup = s.split('e')
        significand = tup[0].rstrip(dec_point)
        sign = tup[1][0].replace(pos_sign, '')
        exponent = tup[1][1:].lstrip('0')
        if not exponent: exponent = 0
        exponent = '10^{%s%s}' % (sign, exponent)
        if significand and exponent:
            s =  r'%s{\times}%s' % (significand, exponent)
        else:
            s =  r'%s%s' % (significand, exponent)
        return "${}$".format(s)

def init_plotter():
    plt.rcParams.update({'font.size': 20})

def plot_values(x_values, x_label, y_values, y_label, precision=2):
    fig, ax = plt.subplots(figsize=(12, 10))  # Create a figure containing a single axes.
    ax.plot(x_values, y_values)  # Plot some data on the axes
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.ticklabel_format(scilimits=(0,0))

    ax.xaxis.set_major_formatter(MathTextSciFormatter(f'%1.{precision}e'))
    ax.yaxis.set_major_formatter(MathTextSciFormatter(f'%1.{precision}e'))

    plt.grid()
    plt.tight_layout()
    plt.show(block=False)

def plot_error_bars(x_values, x_label, y_values, y_label, y_error, x_prec=2, y_prec=2, y_min=None, y_max=None, log=False, save_name=None):
    fig, ax = plt.subplots(figsize=(12, 10))  # Create a figure containing a single axes.
    (_, caps, _) = plt.errorbar(x_values, y_values, yerr=y_error, markersize=6, capsize=20, elinewidth=0.75, linestyle='-',  marker='o')  # Plot some data on the axes
    for cap in caps:
        cap.set_markeredgewidth(1)

    ax.set_ylim([y_min, y_max])
    if log:
        ax.set_yscale('symlog', linthresh=1e-3)
    else:
        ax.ticklabel_format(scilimits=(0,0))
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    ax.xaxis.set_major_formatter(MathTextSciFormatter(f'%1.{x_prec}e'))
    ax.yaxis.set_major_formatter(MathTextSciFormatter(f'%1.{y_prec}e'))

    plt.grid()
    plt.tight_layout()
    if save_name:
        plt.savefig(save_name)
    else:
        plt.show(block=False)

def hold_execution():
    plt.show(block=True)

def regression_slope(data):
    # y = data[i], x = i
    n = len(data)
    if n <= 1:
        return 0

    # Using numpy to multiply arrays
    x = np.linspace(0, n - 1, num=n)
    y = np.array(data)
    
    sum_x, sum_y = np.sum(x), np.sum(y)
    sum_xy, sum_xx = np.sum(x * y), np.sum(x * x)

    denominator = n * sum_xx - (sum_x ** 2)
    if denominator == 0:
        return 0
    numerator = n * sum_xy - sum_x * sum_y
    
    return numerator / denominator

def check_changes(set_1, set_2):
    if len(set_1) < len(set_2):
        small_set = set_1
        big_set = set_2
    else:
        small_set = set_2
        big_set = set_1

    gen_changes = 0
    for cell in small_set:
        if cell not in big_set:
            gen_changes += 1
    gen_changes += abs(len(set_1) - len(set_2))

    return gen_changes