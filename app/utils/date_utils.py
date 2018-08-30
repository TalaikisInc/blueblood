from datetime import datetime, timedelta


def ensure_latest(df):
    latest = df.tail(1).index.strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    ago2 = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    ago3 = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')
    dow = datetime.today().weekday()
    if (dow == 6) | (dow == 0):
        acceptable = [ago3, ago2]
    else:
        acceptable = [ago2, yesterday, today]
    assert latest in acceptable, 'Data isn\'t latest! Expected any of %s, got %s' % (acceptable, latest)
