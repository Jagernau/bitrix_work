from datetime import datetime, timedelta

def get_time_slice():
    past = datetime.utcnow() - timedelta(minutes=30)
    formatted_time_past = past.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    last = datetime.utcnow() + timedelta(minutes=200)
    formatted_time_last = last.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return formatted_time_past, formatted_time_last


