from django.utils import timezone


def format_time_ago(past_time):
    now = timezone.localtime()
    diff = now - past_time

    minutes = diff.total_seconds() / 60
    hours = diff.total_seconds() / 3600
    days = diff.total_seconds() / 86400

    if minutes < 10:
        return f"{int(minutes)}분 전"
    elif minutes < 60:
        return f"{int(minutes // 10 * 10)}분 전"
    elif hours < 24:
        return f"{int(hours)}시간 전"
    else:
        return f"{int(days)}일 전"
