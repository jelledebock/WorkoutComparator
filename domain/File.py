import file_parsers.fitparse
import datetime
import pandas as pd
import os.path


def parse_file(file_path):
    extension = os.path.splitext(file_path)[1]
    if extension == '.csv':
        print("csv file found!")
        return csv_to_df(file_path)
    if extension == '.fit':
        print("fit file found!")
        return fit_to_df(file_path)
    else:
        return None


def fit_to_df(fit_path):
    fitfile = file_parsers.fitparse.FitFile(fit_path)

    power_values = []
    cadence_values = []
    hr_values = []
    lat_values = []
    lon_values = []
    time_values = []

    # Get all data messages that are of type record
    for record in fitfile.get_messages('record'):
            if record.get_value("power"):
                power_values.append(record.get_value("power"))
            else:
                power_values.append(0)
            if record.get_value("cadence"):
                cadence_values.append(record.get_value("cadence"))
            else:
                cadence_values.append(0)
            if record.get_value("timestamp"):
                time_values.append(record.get_value("timestamp"))
            if record.get_value("heart_rate"):
                hr_values.append(record.get_value("heart_rate"))
            else:
                hr_values.append(0)
            if record.get_value("position_lat") and record.get_value("position_long"):
                lat_values.append(semicircles2degrees(record.get_value("position_lat")))
                lon_values.append(semicircles2degrees(record.get_value("position_long")))
            else:
                lat_values.append(0)
                lon_values.append(0)

    epoch = datetime.datetime(1970, 1, 1)

    epoch_values = [int((x-epoch).total_seconds()) for x in time_values]

    columns = ['lat', 'lon', 'timestamp', 'datetime', 'heart_rate', 'cadence', 'power']
    df = pd.DataFrame.from_items(zip(columns, [lat_values, lon_values, epoch_values, time_values, hr_values, cadence_values, power_values]))
    df.fillna(0, inplace=True)
    return df


TWO_POW_31 = float(2147483648)


def semicircles2degrees(value):
    return value*(180.0/TWO_POW_31)


def to_datetime(x):
    return datetime.datetime.utcfromtimestamp(int(x/1000.0))


def to_epoch(x):
    return int(x/1000)


def csv_to_df(csv_file_str):
    csv_file = pd.read_csv(csv_file_str)
    csv_file['timestamp_fmt'] = csv_file['timestamp'].apply(to_datetime)
    csv_file['epoch'] = csv_file['timestamp'].apply(to_epoch)

    columns = ['lat', 'lon', 'timestamp', 'datetime', 'heart_rate', 'cadence', 'power']
    df = csv_file[['latitide', 'longitude', 'epoch', 'timestamp_fmt', 'bpm', 'cadence', 'watts']]
    df.columns = columns
    df.fillna(0,inplace=True)
    return df

