import pymc3 as pm
from pymc3.distributions.timeseries import GaussianRandomWalk
from numpy import exp


def stochastic_vol_model(returns):
    with pm.Model() as model:
        step_size = pm.Exponential('sigma', 50.)
        s = GaussianRandomWalk('s', sd=step_size, shape=len(returns))
        nu = pm.Exponential('nu', .1)
        r = pm.StudentT('r', nu=nu, lam=pm.math.exp(-2*s), observed=returns)
    with model:
        trace = pm.sample(tune=2000, nuts_kwargs=dict(target_accept=.9))
        return exp(trace[s].T)
