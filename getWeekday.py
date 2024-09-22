from datetime import datetime, timedelta

def prev_weekday(adate):
    # Ensure adate is a datetime object
    adate -= timedelta(days=1)
    while adate.weekday() >= 5:  # Sat-Sun are 5-6
        adate -= timedelta(days=1)
    return adate