import domain.File
import pandas as pd

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
            print(file)
            self.linked_dfs.append(domain.File.parse_file(file))

    def get_output(self):
        self.convert_to_dfs()
        for i in range(0, len(self.linked_dfs)):
            df = self.linked_dfs[i]
            label = self.file_labels[i]

            for index, row in df.iterrows():
                if row[self.sort_by] in self.output_object:
                    self.output_object[row[self.sort_by]]['power'].append(row['power'])
                    self.output_object[row[self.sort_by]]['heart_rate'].append(row['heart_rate'])
                    self.output_object[row[self.sort_by]]['cadence'].append(row['cadence'])
                    self.output_object[row[self.sort_by]]['lat'].append(row['lat'])
                    self.output_object[row[self.sort_by]]['lon'].append(row['lon'])
                    self.output_object[row[self.sort_by]]['label'].append(label)
                else:
                    self.output_object[row[self.sort_by]] = {}
                    self.output_object[row[self.sort_by]]['power'] = [row['power']]
                    self.output_object[row[self.sort_by]]['heart_rate'] = [row['heart_rate']]
                    self.output_object[row[self.sort_by]]['cadence'] = [row['cadence']]
                    self.output_object[row[self.sort_by]]['lat'] = [row['lat']]
                    self.output_object[row[self.sort_by]]['lon'] = [row['lon']]
                    self.output_object[row[self.sort_by]]['label'] = [label]

        self.summarize()
        return {'file_labels': self.file_labels, 'values': self.output_object, 'summary': self.summary}

    def summarize(self):
        for i in range(0, len(self.linked_dfs)):
            df = self.linked_dfs[i]
            label = self.file_labels[i]

            avg_power = round(df['power'].mean())
            rolling_power = df['power'].rolling(window=30, center=False).mean()
            normalized_power = round(rolling_power.mean())
            avg_bpm = round(df['heart_rate'].mean())
            avg_cad = round(df['cadence'].mean())

            max_power = round(df['power'].max())
            max_bpm = round(df['heart_rate'].max())
            max_cad = round(df['cadence'].max())

            self.summary[label] = {
                                    "NP": normalized_power,
                                    "max_power": max_power,
                                    "avg_power":avg_power,
                                    "max_heart_rate":max_bpm,
                                    "avg_heart_rate":avg_bpm,
                                    "max_cadence": max_cad,
                                    "avg_cadence":avg_cad
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

