from datetime import datetime


# Converts a time string into seconds
# Throws a ValueError if the string is strangely formatted
def to_ms(value_string):
    if '.' not in value_string:
        value_string += '.0'

    # Check inputted text against all valid formats
    valid_formats = ['%H:%M:%S.%f', '%M:%S.%f', '%S.%f']
    for test_format in valid_formats:
        try:
            dt = datetime.strptime(value_string, test_format)
            return int(dt.hour * 3600000 + dt.minute * 60000 + dt.second * 1000 + dt.microsecond / 1000)
        except ValueError:
            pass

    # Unknown format
    raise ValueError


# Converts ms to a time string
def to_time(ms):
    # Compute hours, minutes, seconds, and milleseconds
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)

    if ms == 0:
        ms_part = ''
    else:
        ms_part = f'.{ms:03d}'

    # Print the string depending on what kind of time it is
    if not h == 0:
        return f'{h}:{m:02d}:{s:02d}{ms_part}'
    elif not m == 0:
        return f'{m}:{s:02d}{ms_part}'

    return f'{s}{ms_part}s'
