from datetime import datetime, timedelta


def get_time(string_format=False, **kwargs):
    date_time = datetime.now() + timedelta(**kwargs)
    if string_format:
        return time_to_string(date_time)
    else:
        return date_time


def time_to_string(date_time, format_date="%Y-%m-%d %H:%M:%S") -> str:
    return date_time.strftime(format_date)
