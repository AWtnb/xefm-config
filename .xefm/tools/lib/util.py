import datetime


def get_timestamp() -> str:
    tz_jst = datetime.timezone(datetime.timedelta(hours=9))
    return datetime.datetime.now(tz=tz_jst).strftime("%Y%m%d-%H%M%S")
