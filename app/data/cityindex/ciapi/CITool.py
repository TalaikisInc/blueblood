import time


def wcfDate2Sec(wcf_date):
    timeMS = wcf_date.split("(")
    if len(timeMS) > 0:
        timeMS = timeMS[1].split(")")
        if len(timeMS) > 0:
            timeMS = timeMS[0]
        else:
            timeMS = "0"
    else:
        timeMS = "0"
    return float(timeMS) / 1e3


def time2str(time_sec, localTimeFlag=False):
    if localTimeFlag:
        time_struct = time.localtime(time_sec)
    else:
        time_struct = time.gmtime(time_sec)
    return time.strftime('%Y-%m-%d %H:%M:%S', time_struct)


def intervalUnitSec(context):
    str = context.TimeInterval
    if (str == "HOUR"):
        return 3600
    elif (str == "MINUTE"):
        return 60
    elif (str == "DAY"):
        return 86400
