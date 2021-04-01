import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

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
        if exponent:
            exponent = '10^{%s%s}' % (sign, exponent)
        if significand and exponent:
            s =  r'%s{\times}%s' % (significand, exponent)
        else:
            s =  r'%s%s' % (significand, exponent)
        return "${}$".format(s)

def plot_values(x_values, x_label, y_values, y_label, precision=2):
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(x_values, y_values)  # Plot some data on the axes
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.ticklabel_format(scilimits=(0,0))

    ax.xaxis.set_major_formatter(MathTextSciFormatter(f'%1.{precision}e'))
    ax.yaxis.set_major_formatter(MathTextSciFormatter(f'%1.{precision}e'))

    plt.grid()
    plt.show(block=False)

def hold_execution():
    plt.show(block=True)