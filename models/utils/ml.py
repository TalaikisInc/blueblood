from dask_ml import joblib
from sklearn.externals.joblib import parallel_backend

def run(code):
    with parallel_backend('dask'):
        code()

def xgboost(data, labels):
    from dask_ml.xgboost import XGBRegressor

    estimator = XGBRegressor()
    return estimator.fit(data, labels)
