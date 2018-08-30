from numpy import random, dot, array, eye, asarray, vstack, ones, expand_dims
from filterpy.kalman import EnsembleKalmanFilter
from pykalman import KalmanFilter
from filterpy.kalman import KalmanFilter
from matplotlib import pyplot as plt
from pandas import Series
random.seed(1234)


def hx(x):
    return array([x[0]])

def fx(x, dt):
    return dot(F, x)

def kalman():
    filter = KalmanFilter(dim_x=2, dim_z=1)
    x = array([0., 1.])
    P = eye(2) * 100.
    enf = EnsembleKalmanFilter(x=x, P=P, dim_z=1, dt=1., N=20, hx=hx, fx=fx)

    measurements = []
    results = []
    ps = []
    kf_results = []
    for i in range(len(data)):
        z = data.iloc[i].as_array()
        enf.predict()
        enf.update(asarray([z]))
        filter.predict()
        filter.update(asarray([[z]]))

        results.append (enf.x[0])
        kf_results.append (kf.x[0,0])
        measurements.append(z)
        ps.append(3*(enf.P[0,0]**.5))
    results = asarray(results)
    ps = asarray(ps)

def plot(results, kf_results, measurements, ps):
    plt.plot(results, label='EnKF')
    plt.plot(kf_results, label='KF', c='b', lw=2)
    plt.plot(measurements, 'kx')
    plt.plot (results - ps, c='k',linestyle=':', lw=1, label='1$\sigma$')
    plt.plot(results + ps, c='k', linestyle=':', lw=1)
    plt.fill_between(range(len(results)), results - ps, results + ps, facecolor='y', alpha=.3)
    plt.legend(loc='best');
    plt.show()

def kalman_average(x):
  kf = KalmanFilter(transition_matrices=[1], observation_matrices=[1], initial_state_mean=0,
     initial_state_covariance=1, observation_covariance=1, transition_covariance=.01)
  state_means, _ = kf.filter(x.values)
  state_means = Series(state_means.flatten(), index=x.index)
  return state_means

def kalman_regression(x, y):
  delta = 1e-3
  # How much random walk wiggles
  trans_cov = delta / (1 - delta) * eye(2)
  obs_mat = expand_dims(vstack([[x], [ones(len(x))]]).T, axis=1)

  kf = KalmanFilter(n_dim_obs=1, n_dim_state=2, initial_state_mean=[0,0], initial_state_covariance=ones((2, 2)), transition_matrices=eye(2),
     observation_matrices=obs_mat, observation_covariance=2, transition_covariance=trans_cov)
  state_means, state_covs = kf.filter(y.values)
  return state_means
