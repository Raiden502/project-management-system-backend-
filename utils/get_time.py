from datetime import datetime, timedelta
import pytz


def getCurrentTime():
    timezone = pytz.timezone('Asia/Kolkata')
    time = datetime.now(tz=timezone)
    return time.strftime('%Y-%m-%d %H:%M:%S')


def setExpirationTime():
    timezone = pytz.timezone("Asia/Kolkata")
    time = datetime.now(tz=timezone)
    newtime = time + timedelta(seconds=60)
    return newtime.strftime("%Y-%m-%d %H:%M:%S")


def setTimeAfterResend():
    timezone = pytz.timezone("Asia/Kolkata")
    time = datetime.now(tz=timezone)
    newtime = time + timedelta(minutes=2)
    return newtime.strftime("%Y-%m-%d %H:%M:%S")
