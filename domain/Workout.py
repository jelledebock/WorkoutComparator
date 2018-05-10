import domain.File
import pandas as pd
import json
import math
import os
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


class Session:
    def __init__(self, name):
        self.name = name
        self.linked_files = []
        self.linked_dfs = []
        self.file_labels = []
        self.output_object = {}
        self.summary = {}
        self.sort_by = "timestamp"

    def add_file(self, file_path, file_label):
        self.linked_files.append(file_path)
        self.file_labels.append(file_label)

    def convert_to_dfs(self):
        for file in self.linked_files:
            self.linked_dfs.append(domain.File.parse_file(file))

    def get_output(self, summary_location, dfs_location):
        self.convert_to_dfs()
        for i in range(0, len(self.linked_dfs)):
            df = self.linked_dfs[i]
            label = self.file_labels[i]

            os.makedirs(os.path.dirname(dfs_location+'/'+label+'.csv'), exist_ok=True)
            df.to_csv(os.path.join(dfs_location, label+'.csv'), index=False, na_rep=0)

        self.summarize()
        os.makedirs(os.path.dirname(summary_location), exist_ok=True)

        with open(summary_location, 'w') as ofile:
            ofile.write(json.dumps({'file_labels': self.file_labels, 'summary': self.summary, "sort_by": self.sort_by}, cls=NumpyEncoder))

    def summarize(self):
        for i in range(0, len(self.linked_dfs)):
            df = self.linked_dfs[i]
            label = self.file_labels[i]

            has_power = df['power'].sum()>0
            avg_power = round(df['power'].mean())
            rolling_power = df['power'].rolling(window=30, center=False).mean().pow(4)
            normalized_power = round(math.pow(rolling_power.mean(), 0.25))
            print(normalized_power)

            has_hr = df['heart_rate'].sum()>0
            avg_bpm = round(df['heart_rate'].mean())

            has_cad = df['cadence'].sum()>0
            avg_cad = round(df['cadence'].mean())

            max_power = round(df['power'].max())
            max_bpm = round(df['heart_rate'].max())
            max_cad = round(df['cadence'].max())

            outdoor_or_virtual = df['lat'].sum()>0

            self.summary[label] = {
                                    "has_power": int(has_power),
                                    "has_cadence": int(has_cad),
                                    "has_hr": int(has_hr),
                                    "outdoor_or_virtual": int(outdoor_or_virtual),
                                    "NP": normalized_power,
                                    "max_power": max_power,
                                    "avg_power":avg_power,
                                    "max_heart_rate":max_bpm,
                                    "avg_heart_rate":avg_bpm,
                                    "max_cadence": max_cad,
                                    "avg_cadence":avg_cad,
            }



class DateTimeSession(Session):
    def __init__(self, name):
        Session.__init__(self, name)
        self.sort_by = "timestamp"


class DistanceSession(Session):
    def __init__(self, name):
        Session.__init__(self, name)
        self.sort_by = "Distance"


class DurationSession(Session):
    def __init__(self, name):
        Session.__init__(self, name)
        self.sort_by = "Duration"

