from os.path import join
from os import remove

from sklearn.model_selection import TimeSeriesSplit
from sklearn.utils import indexable
from sklearn.utils.validation import _num_samples
from numpy import arange

from .file_utils import filenames
from .vars import STORAGE_PATH


def train_test_split(data, part=0.7):
    ''' Splits data into tain and test sets. '''
    train = data.iloc[:int(len(data.index)*part)]
    test = data.iloc[int(len(data.index)*part):]
    return (train, test)

def count_splits(folder):
    ''' Counts total split files in _splits of the directory. '''
    return len(filenames(join(folder, '_split')))

def clean_splits(folder):
    ''' Cleans split files in _splits of the directory. '''
    path = join(folder, '_split')
    fs = filenames(path)
    for f in fs:
        remove(join(STORAGE_PATH, path, f))

class TimeSeriesSplitImproved(TimeSeriesSplit):
    def split(self, X, y=None, groups=None, fixed_length=False, train_splits=1, test_splits=1):
        """Generate indices to split data into training and test set.
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training data, where n_samples is the number of samples
            and n_features is the number of features.
        y : array-like, shape (n_samples,)
            Always ignored, exists for compatibility.
        groups : array-like, with shape (n_samples,), optional
            Always ignored, exists for compatibility.
        fixed_length : bool, hether training sets should always have
            common length
        train_splits : positive int, for the minimum number of
            splits to include in training sets
        test_splits : positive int, for the number of splits to
            include in the test set
        Returns
        -------
        train : ndarray
            The training set indices for that split.
        test : ndarray
            The testing set indices for that split.
        """
        X, y, groups = indexable(X, y, groups)
        n_samples = _num_samples(X)
        n_splits = self.n_splits
        n_folds = n_splits + 1
        train_splits, test_splits = int(train_splits), int(test_splits)
        if n_folds > n_samples:
            raise ValueError('Cannot have number of folds ={0} greater than the number of samples: {1}.'.format(n_folds, n_samples))
        if (n_folds - train_splits - test_splits) > 0 and (test_splits > 0):
            raise ValueError('Both train_splits and test_splits must be positive integers.')
        indices = arange(n_samples)
        split_size = (n_samples // n_folds)
        test_size = split_size * test_splits
        train_size = split_size * train_splits
        test_starts = range(train_size + n_samples % n_folds, n_samples - (test_size - split_size), split_size)
        if fixed_length:
            for i, test_start in zip(range(len(test_starts)), test_starts):
                rem = 0
                if i == 0:
                    rem = n_samples % n_folds
                yield (indices[(test_start - train_size - rem):test_start], indices[test_start:test_start + test_size])
        else:
            for test_start in test_starts:
                yield (indices[:test_start], indices[test_start:test_start + test_size])
