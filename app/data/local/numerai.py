from os.path import join

from pandas import read_csv, DataFrame
from clint.textui import colored

from utils import STORAGE_PATH


def download():
    pass

def data():
    train = read_csv('data/numerai_training_data.csv')
    test = read_csv('data/numerai_tournament_data.csv')
    
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
