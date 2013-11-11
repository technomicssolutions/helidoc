from django import template
from decimal import Decimal
from dateutil.relativedelta import relativedelta
import re
register = template.Library()
import datetime


def IsNumber(x):
    if re.match("^\d*.?\d*$", x) == None:
        return False
    return True

def split(value,arg):
    if (value):
        rr=value.split(arg)
    else:
        return None
    if not rr[0]:
        return None
    else:
        return value.split(arg)

def splitfilename(value,arg):
    return value.split('|')[int(arg)]

def subdatcon(value,arg):
        return str(round(Decimal(value)-Decimal(arg),1))

def adddatcon(value,arg):
    return str(round(Decimal(value)+Decimal(arg),1))

def addmaintime(value,arg):
    r=value
    if arg and len(arg)>1:
        if IsNumber(arg[:-1]):
            if arg.lower().endswith('m'):
                m={'months':int(arg[:-1])}
            elif arg.lower().endswith('y'):
                m={'years':int(arg[:-1])}
            else:
                m={'days':int(arg[:-1])}
            r=value+relativedelta(**m)-relativedelta(days=1)
    return r

def daysfromtoday(value,arg):
    if arg:
        today=arg
    else:
        today=datetime.date.today()
    return (value-today).days

def endswith(value,arg):
    return value.endswith(arg)

def ltfloat(a,b):
    return float(a)<float(b)

register.filter('subdatcon', subdatcon)
register.filter('adddatcon', adddatcon)
register.filter('addmaintime', addmaintime)

register.filter('split', split)
register.filter('splitfilename', splitfilename)
register.filter('daysfromtoday', daysfromtoday)
register.filter('endswith', endswith)
register.filter('ltfloat', ltfloat)

