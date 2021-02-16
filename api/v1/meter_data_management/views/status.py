__author__ = "aki"


def check_meter_status(value):
    if value == 'OK':
        return 0
    elif value == 'NO-DISPLAY':
        return 1
    elif value == 'METER-MISSING':
        return 2
    elif value == 'PERMANENT-DISCONNECTION':
        return 3
    elif value == 'DISCONNECTION':
        return 4
    elif value == 'METER-STOLEN':
        return 5
    elif value == 'DISPLAY-OUT':
        return 6
    elif value == 'METER-CHANGED':
        return 7
    elif value == 'GLASS-BROKEN':
        return 8
    elif value == 'METER-BRUNT':
        return 9
    else:
        return False
