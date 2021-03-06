import file_parsers.fitparse
import datetime
import pandas as pd
import os.path
import domain.Workout


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
    print(time_values[0])
    epoch_values = [(x-epoch).total_seconds() for x in time_values]

    columns = ['lat', 'lon', 'timestamp', 'datetime', 'heart_rate', 'cadence', 'power']
    df = pd.DataFrame.from_items(zip(columns, [lat_values, lon_values, epoch_values, time_values, hr_values, cadence_values, power_values]))
    df.fillna(0, inplace=True)
    print(df)
    return df


TWO_POW_31 = float(2147483648)


def set_offset_seconds(df, seconds):
    df['timestamp']=df['timestamp'] + seconds


def get_df(json, file):
    columns = ['lat', 'lon', 'timestamp', 'datetime', 'heart_rate', 'cadence', 'power']
    df = pd.DataFrame(columns=columns)
    for key in json['values']:
        value = json['values'][key]
        pos_in_labels = -1
        i=0
        for label in value['label']:
            if label == file:
                pos_in_labels = i
            i+=1

        if pos_in_labels != -1:
            df.append([             value['lat'][pos_in_labels],
                                    value['lon'][pos_in_labels],
                                    key,
                                    value['heart_rate'][pos_in_labels],
                                    value['power'][pos_in_labels],
                                    value['cadence'][pos_in_labels]
                      ])

    time_session_obj = domain.Workout.DateTimeSession()

    return df


def get_x_y_values(df, x, y):
    output = []
    for index, row in df.iterrows():
        output.append({'x': row[x], 'y': row[y]})

    return output


def modify_with_offset(df_file, offset):
    df = pd.read_csv(df_file)
    df['timestamp']=df['timestamp'].apply(lambda x: float(x) + float(offset))
    df.to_csv(df_file, index=False)

def semicircles2degrees(value):
    return value*(180.0/TWO_POW_31)


def to_datetime(x):
    return datetime.datetime.utcfromtimestamp(int(x/1000.0))


def to_epoch(x):
    return int(x/1000.0)


def csv_to_df(csv_file_str):
    csv_file = pd.read_csv(csv_file_str)
    csv_file['timestamp_fmt'] = csv_file['timestamp'].apply(to_datetime)
    csv_file['epoch'] = csv_file['timestamp'].apply(to_epoch)

    columns = ['lat', 'lon', 'timestamp', 'datetime', 'heart_rate', 'cadence', 'power']
    df = csv_file[['latitide', 'longitude', 'epoch', 'timestamp_fmt', 'bpm', 'cadence', 'watts']]
    df.columns = columns
    df.fillna(0, inplace=True)
    return df

