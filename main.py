import domain.File
import domain.Workout
import json
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


files = domain.Workout.DateTimeSession('Test P2M and Neo')
files.add_file('/home/jelle/Desktop/2018-04-30-18-27-12.fit', 'Tacx Neo')
files.add_file('/home/jelle/Desktop/2018-04-30-162736-ELEMNT CE5F-262-12.fit', 'Power2Max NG Eco')

with open('./out.json', 'w') as ofile:
    ofile.write(json.dumps(files.get_output(), cls=NumpyEncoder))
