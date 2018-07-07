def train_test_split(data, part=0.7):
    train = data.iloc[:int(len(data.index)*part)]
    test = data.iloc[int(len(data.index)*part):]
    return (train, test)
