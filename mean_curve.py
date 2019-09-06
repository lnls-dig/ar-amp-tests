import argparse
import numpy as np
import matplotlib.pyplot as plt
import sympy
import sympy.abc

parser = argparse.ArgumentParser()
parser.add_argument('data', type=str, nargs='+', help='Data to be plotted')
parser.add_argument('-f', '--fit', action='store_true', help='Fit polynomial curve to data')
parser.add_argument('-d', '--degree', help='Polynomial degree', default=4)
args = parser.parse_args()

y_acc = np.zeros(512)
x_acc = np.zeros(512)

for data_file in args.data:
    x, y = np.loadtxt(data_file, skiprows=1, unpack=True)
    #Attenuator offset
    y = y + 30.0
    x, y = y, x
    y_acc += y
    x_acc += x

    if args.fit:
        p = np.poly1d(np.polyfit(x, y, args.degree))
        t = np.linspace(x[0],x[-1], 4096)
        plt.plot(t, p(t), '-', label=data_file)
    else:
        plt.plot(x, y, '.', label=data_file)

#x_acc, y_acc = y_acc, x_acc
y_acc = y_acc/len(args.data)
x_acc = x_acc/len(args.data)
plt.plot(x_acc, y_acc, '.', label='Acc')

if args.fit:
    p = np.poly1d(np.polyfit(x_acc, y_acc, args.degree))
    t = np.linspace(x_acc[0],x_acc[-1], 4096)
    print(p.c)
    p_str = sympy.latex(sympy.Poly(p.c, sympy.abc.x).as_expr())
    plt.plot(t, p(t), '-', label="Mean: ${}$".format(p_str))
    print(p_str)
else:
    plt.plot(x, y, '.', label='Mean')

plt.legend(loc='upper left')
plt.show()
