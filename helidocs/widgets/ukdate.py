from pytz import timezone
import datetime

def ukdate():
    utc=timezone('UTC')
    uk=timezone('Europe/London')
    r=utc.localize(datetime.datetime.utcnow())
    return r.astimezone(uk)


def ukdatetime():
    utc=timezone('UTC')
    uk=timezone('Europe/London')
    r=utc.localize(datetime.datetime.utcnow())
    return r.astimezone(uk)
