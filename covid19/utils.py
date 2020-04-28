import json
import numpy as np
import enum
import os
import datetime

class JsonEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """

    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32,
                              np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        elif isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, enum.Enum):
            return obj.name
        else:
            try:
                return obj.__dict__
            except Exception:
                print(f'{obj} is not serializable. ')
                return f'Object not serializable - {obj}'


def file_exists_check(filepath: str, err_msg:str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(err_msg)


def calc_n_days_before_date(date_str, n_days):
    # date_str is in the format 'm/day/year'
    strs = date_str.split('/')
    month, date, year = strs[0], strs[1], strs[2]
    date = datetime.datetime(year, month, date)
    rolled_back_date = date - datetime.timedelta(days=n_days)
    # Return in the same format as recieved
    return f'{rolled_back_date.month}/{rolled_back_date.day}/{rolled_back_date.year}'


def calc_n_days_after_date(date_str, n_days):
    # date_str is in the format 'm/day/year'
    strs = date_str.split('/')
    month, day, year = strs[0], strs[1], strs[2]
    date = datetime.datetime(int(year), int(month), int(day))
    future_date = date + datetime.timedelta(days=n_days)
    # Return in the same format as recieved
    return f'{future_date.month}/{future_date.day}/{future_date.year}'

