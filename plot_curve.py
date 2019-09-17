import csv
import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

parser = argparse.ArgumentParser()
parser.add_argument('data', type=str, nargs='+', help='Data to be plotted')
parser.add_argument('-y', '--y_label', default= 'Gain [step]', type=str, help='Y Axis label')
parser.add_argument('-x', '--x_label', default='Gain [dB]', type=str, help='X Axis label')
parser.add_argument('-d', '--degree', default=4, type=int, help='Fit polynomial degree')
parser.add_argument('-f', '--fit', action='store_true', help='Fit polynomial curve to data')
parser.add_argument('--hide_data', action='store_true', help='Hide original data plot (plot only fit)')
args = parser.parse_args()

def logistic4(x, A, B, C, D):
    """4PL lgoistic equation."""
    #return ((A-D)/(1.0+((x/C)**B))) + D
    return A + ((B - A)/(1 + 10**((C-x)*D)))

for i, data_file in enumerate(args.data):
    reader = csv.reader(open(data_file,'rb'), delimiter=',')
    reader_list = list(reader)
    step, pot = np.array(reader_list).astype('float').T
    pot = pot + 50.0

    if not args.hide_data:
        plt.plot(pot, step, 'o')

    if args.fit:
        #popt, pcov = curve_fit(logistic4, x, y)
        p = np.poly1d(np.polyfit(pot, step, args.degree))
        t = np.linspace(pot[0],pot[-1], 4096)
        plt.plot(t, p(t), '-', label=data_file)
        #plt.plot(x, logistic4(x, *popt), '-', label=data_file)

plt.title('AR Amplifiers gain curve')
plt.legend(loc='upper left')
plt.ylabel(args.y_label)
plt.xlabel(args.x_label)
plt.show()
