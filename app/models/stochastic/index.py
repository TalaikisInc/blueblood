from stochastic.discrete import BernoulliProcess
from stochastic.continuous import FractionalBrownianMotion, BrownianMotion
from stochastic.diffusion import CoxIngersollRossProcess


def bernouli(p=0.7, n=300):
    model = BernoulliProcess(p=p)
    times = model.times(n)
    samples = model.sample(n)
    return (times, samples)

def brownian(t=1, drift=0, scale=1, n=300):
    model = BrownianMotion(t=t, dift=drift, scale=1)
    times = model.times(n)
    samples = model.sample(n)
    return (times, samples)

def fractional_brownian(t=1, hurst=0.7, n=300):
    model = FractionalBrownianMotion(t=t, hurst=hurst)
    times = model.times(n)
    samples = model.sample(n)
    return (times, samples)

def cir(t=1, n=300):
    model = CoxIngersollRossProcess(t=t)
    times = model.times(n)
    samples = model.sample(n)
    return (times, samples)
