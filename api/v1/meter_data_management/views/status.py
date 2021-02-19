__author__ = "aki"


def check_meter_status(value):
    if value == 'NORMAL':
        return 0
    elif value == 'FAULTY':
        return 1
    elif value == 'RCNT':
        return 2
    else:
        return False
