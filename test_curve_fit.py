import math

from numpy import log
from scipy.optimize import curve_fit


def f_model(x, A, n, E):
    # print(x, A, n, E)
    return log(A)+n*log(x)-E/(x*1.9872)


# popt, pcov = curve_fit(f=f_model, xdata=xdata, ydata=ydata, p0=(3, -2, 1),)
def fitnlm(xdata, ydata, f_model):
    popt, pcov = curve_fit(f=f_model, xdata=xdata, ydata=ydata, maxfev = 8000)
    return popt

def get_curve_value(xdata, ydata):
    try:
        ln_ydata = [math.log(y) for y in ydata]
        data = fitnlm(xdata, ln_ydata, f_model)
        fit_y = [math.e**f_model(x,*data)for x in xdata]
        fit_y = [round(number, 4) for number in fit_y]
    except:
        # when can not fit the curve
        fit_y = [0 for i in range(len(ydata))]
    return fit_y
