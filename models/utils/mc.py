import pymc3 as pm

def gen():
    with pm.Model() as model:
        mu = pm.Normal('mu', mu=0, sd=1)
        obs = pm.Normal('obs', mu=mu, sd=1, observed=np.random.randn(100))