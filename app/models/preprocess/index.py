from sklearn.preprocessing import Binarizer


def binarize(data, threshold):
    bn = Binarizer(threshold=threshold)
    return bn.transform([data])[0]
