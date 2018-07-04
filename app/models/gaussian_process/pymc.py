from pymc3 import Model, Gamma, gp, HalfCauchy
import theano.tensor as tt


def gaussian(x, y):
    X = x.reshape(-1, 1)
    Z = linspace(-6, 6, 100).reshape(-1, 1)
    with Model() as gp_fit:
        ρ = Gamma('ρ', 1, 1)
        nu = Gamma('nu', 1, 1)
        K = nu * gp.cov.Matern32(1, ρ)
    with gp_fit:
        M = gp.mean.Zero()
        σ = HalfCauchy('σ', 2.5)
    with gp_fit:
        y_obs = gp.GP('y_obs', mean_func=M, cov_func=K, sigma=σ, observed={'X': X, 'Y': y})
    with gp_fit:
        gp_samples = pm.gp.sample_gp(trace[1000:], y_obs, Z, samples=50)
