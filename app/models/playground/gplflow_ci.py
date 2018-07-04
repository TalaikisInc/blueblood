import gpflow
from numpy import linspace, sqrt
from matplotlib import pyplot as plt

def model(X, Y):
    k = gpflow.kernels.Matern52(1, lengthscales=0.3)
    m = gpflow.models.GPR(X, Y, kern=k)
    m.likelihood.variance = 0.01
    return m

def plot(model, X, Y, out_sample):
    mean, var = model.predict_y(out_sample)
    plt.figure(figsize=(12, 6))
    plt.plot(X, Y, 'kx', mew=2)
    plt.plot(out_sample, mean, 'C0', lw=2)
    plt.fill_between(xx[:,0],
        mean[:, 0] - 2 * sqrt(var[:, 0]),
        mean[:, 0] + 2 * sqrt(var[:, 0]),
        color='C0', alpha=0.2)
    plt.xlim(-0.1, 1.1)
    plt.show()
