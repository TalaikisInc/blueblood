from os.path import join
from os import getenv
from operator import itemgetter

from pandas import read_csv, DataFrame
from clint.textui import colored
from numerapi import NumerAPI

from app.utils import STORAGE_PATH


def getapi():
    return NumerAPI(getenv('NUMERAI_ID'), getenv('NUMERAI_SECRET'))

def get_data():
    api = getapi()
    last = _last_round(api)
    train = read_csv(join(STORAGE_PATH, 'numerai',  last, 'numerai_training_data.csv'))
    test = read_csv(join(STORAGE_PATH, 'numerai', last, 'numerai_tournament_data.csv'))

    features = [f for f in list(train) if 'feature' in f]
    X_train = train[features]
    Y_train = train.target
    X_test = test[features]
    ids = test['id']

    X_valid = test.ix[test['data_type'] == 'validation', features]
    Y_valid = test.ix[test['data_type'] == 'validation', 'target']

    return X_train, Y_train, X_valid, Y_valid, X_test, ids

def write_predictions(predicted, ids):
    api = getapi()
    last = _last_round(api)
    filename = '{}_predictions.csv'.format(last)
    res = DataFrame({'id': ids, 'probability': list(predicted)})
    res.to_csv(join(STORAGE_PATH, 'numerai', filename), index=False)
    print(colored.green('Results saved'))

def _last_round(api):
    rounds = api.get_competitions()
    return max([i['number'] for i in rounds])

def download_dataset():
    api = getapi()
    last = _last_round(api)
    api.download_current_dataset(unzip=True, dest_path=join(STORAGE_PATH, 'numerai'), dest_filename='{}'.format(last))

    if api.check_new_round():
        print('New round has started, downloading data')
    
def upload_precictions():
    api = getapi()
    last = _last_round(api)
    api.upload_predictions(join(STORAGE_PATH, 'numerai', '{}_predictions.csv'.format(last)))
    api.submission_status()
