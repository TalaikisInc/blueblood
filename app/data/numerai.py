from os.path import join
from os import getenv
from operator import itemgetter

from pandas import read_csv, DataFrame
from clint.textui import colored
from numerapi import NumerAPI

from app.utils import STORAGE_PATH


def getapi():
    return NumerAPI(getenv('NUMERAI_ID'), getenv('NUMERAI_SECRET'))

def get_numerai_data():
    api = getapi()
    last = _last_round(api)
    train = read_csv(join(STORAGE_PATH, 'numerai',  '{}'.format(last), 'numerai_training_data.csv'))
    test = read_csv(join(STORAGE_PATH, 'numerai', '{}'.format(last), 'numerai_tournament_data.csv'))

    features = [f for f in list(train) if 'feature' in f]
    X_train = train[features]
    target_col = [t for t in list(train) if 'target' in t][0]
    Y_train = train[target_col]
    X_test = test[features]
    ids = test['id']

    return X_train, Y_train, X_test, ids

def write_numerai_predictions(predicted, ids):
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
