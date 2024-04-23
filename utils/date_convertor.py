from datetime import datetime


def days_until_target_date(target_date_str):
    target_date = datetime.strptime(target_date_str, "%Y-%m-%dT%H:%M:%S")
    current_date = datetime.now()
    remaining_time = target_date - current_date
    days_remaining = remaining_time.days
    return days_remaining