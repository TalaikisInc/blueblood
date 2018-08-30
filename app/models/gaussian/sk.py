from numpy import exp, subtract, linalg, linspace
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel

def gaussian_process(x, y):
    X = x.reshape(-1, 1)
    kernel = ConstantKernel() + Matern(length_scale=2, nu=3/2) + WhiteKernel(noise_level=1)
    gp = GaussianProcessRegressor(kernel=kernel)
    est = gp.fit(X, y)
    x_pred = linspace(-6, 6).reshape(-1, 1)
    y_pred, sigma = gp.predict(x_pred, return_std=True)
    return (y_pred, sigma)
