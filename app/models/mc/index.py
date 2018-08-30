import pymc3 as pm
from scipy.stats import t


def gen():
    with pm.Model() as model:
        mu = pm.Normal('mu', mu=0, sd=1)
        obs = pm.Normal('obs', mu=mu, sd=1, observed=np.random.randn(100))

def mc_fit(data):
    return t.fit(data)

def mc_roll(params):
    return t.rvs(df=int(params[0]), loc=params[1], scale=params[2], size=100000)
