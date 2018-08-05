from os.path import join
from os import getenv

from pandas import read_csv, DataFrame
from clint.textui import colored
from numerapi import NumerAPI

from app.utils import STORAGE_PATH


def download():
    pass

def data():
    train = read_csv(join('data/numerai_training_data.csv'))
    test = read_csv(join('data/numerai_tournament_data.csv'))
    
    features = [f for f in list(train) if 'feature' in f]
    X = train[features]
    Y = train.target
    X_test = test[features]
    ids = test['id']
    
    X_valid = test.ix[test['data_type'] == 'validation', features]
    Y_valid = test.ix[test['data_type'] == 'validation', 'target']
    
    return X, Y, X_valid, Y_valid, X_test, ids

def write(prediced, ids, filename):
    res = DataFrame({'id': ids, 'probability': list(prediced)})
    res.to_csv(join(STORAGE_PATH, 'numerai', filename), index=False)
    print(colored.green('Results saved to %s' % filepath))

def download_dataset():
    api = NumerAPI(verbosity='info')
    api.download_current_dataset(unzip=True)

    if api.check_new_round():
        print("new round has started wihtin the last 24hours!")
    else:
        print("no new round within the last 24 hours")

def upload_precictions():
    api = NumerAPI(getenv('NUMERAI_ID'), getenv('NUMERAI_SECRET'))
    submission_id = api.upload_predictions(join(STORAGE_PATH, 'numerai', '_predictions.csv'))
    api.submission_status()
