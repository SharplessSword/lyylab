from numpy import log
from scipy.optimize import curve_fit

def f_model(x, A, n, E):
    # print(x, A, n, E)
    return log(A)+n*log(x)-E/(x*1.9872)


# popt, pcov = curve_fit(f=f_model, xdata=xdata, ydata=ydata, p0=(3, -2, 1),)
def fitnlm(xdata, ydata, f_model):
    popt, pcov = curve_fit(f=f_model, xdata=xdata, ydata=ydata, maxfev = 8000)
    return popt

# xdata = [250, 298, 400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
