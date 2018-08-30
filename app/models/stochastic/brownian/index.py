from random import gauss

from numpy import exp, zeros, float64, random, sqrt, linspace, array, random, cumsum
import matplotlib.pyplot as plt
from pandas import DataFrame

def BP(seed, N):
    dt = 1./N                                    # time step
    b = random.normal(0., 1., int(N))*sqrt(dt)  # brownian increments
    W = cumsum(b)                             # brownian path
    return W, b


def GBM(S0, mu, sigma, T, N, seed):
    W = BP(seed, N)[0]
    t = linspace(0., 1., N+1)
    S = []
    S.append(S0)
    for i in range(1,int(N+1)):
        drift = (mu - 0.5 * sigma**2) * t[i]
        diffusion = sigma * W[i-1]
        S_temp = S0 * exp(drift + diffusion)
        S.append(S_temp)
    return array(S), array(t)


def gen_paths(I, S0, mu, sigma, T, N, seed):
    """
    S0 = 1000
    mu = 0.6
    sigma = 0.2
    T = 1/252 #time period
    N = 252 #steps
    paths = 300
    gen_paths(I=paths, S0=S0, mu=mu, sigma=sigma, T=T, N=N, seed=seed)
    """
    paths = []
    for i in range(I):
        path = GBM(S0=S0, mu=mu, sigma=sigma, T=T, N=N, seed=seed)
        paths.append({ "idx": path[1], "val": path[0] })
        plt.plot(path[1], path[0])
    plt.axhline(S0)
    plt.show()
    return paths
