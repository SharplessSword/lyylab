import math

from numpy import log
from scipy.optimize import curve_fit


def f_model(x, A, n, E):
    # print(x, A, n, E)
    return log(A) + n * log(x) - E / (x * 1.9872)


# popt, pcov = curve_fit(f=f_model, xdata=xdata, ydata=ydata, p0=(3, -2, 1),)
def fitnlm(xdata, ydata, f_model):
    popt, pcov = curve_fit(f=f_model, xdata=xdata, ydata=ydata, maxfev=8000)
    return popt


def get_curve_value(xdata, ydata, select_xdata):
    try:
        fit_part_xdata = []
        fit_part_ydata = []
        for i in range(len(select_xdata)):
            if select_xdata[i] == '1':
                fit_part_xdata.append(xdata[i])
                fit_part_ydata.append(ydata[i])
        ln_ydata = [math.log(y) for y in fit_part_ydata]
        data = fitnlm(fit_part_xdata, ln_ydata, f_model)
        A, n, E = [beautify_number(i) for i in data]
        fit_y = [math.e ** f_model(x, *data) for x in xdata]
        fit_y = [beautify_number(number) for number in fit_y]
    except:
        # when can not fit the curve
        fit_y = [0 for i in range(len(ydata))]
        A, n, E = 0, 0, 0
    return fit_y, A, n, E


def beautify_number(number):
    abs_number = abs(number)
    if abs_number > 10000 or abs_number < 0.0001:
        number = format(number, '0.3e')
    elif 10000 >= abs_number > 10:
        number = format(number, '0.1f')
    else:
        number = format(number, '0.3f')
    return number


def extract_fit_part(xdata, ydata):
    fit_part_xdata = []
    fit_part_ydata = []
    for i in range(len(ydata)):
        if ydata[i] != -1:
            fit_part_xdata.append(xdata[i])
            fit_part_ydata.append(ydata[i])
