import datetime


def get_written_days_from_date(d, ref_date=datetime.date.today(), include_date=False):
    delta = (d - ref_date).days

    if delta == 0:
        message = 'Today'
    elif delta == -1:
        message = 'Yesterday'
    elif delta == 1:
        message = 'Tomorrow'
    elif delta < 0:
        message = f'{-delta} days ago'
    else:
        message = f'in {delta} days'

    if include_date:
        message += f' ({d.strftime("%b %d")})'

    return message
