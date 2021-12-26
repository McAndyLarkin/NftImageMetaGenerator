import sys
import os
import json


def replace(newUrl, path):
    for item in os.listdir(path):
        with open(path + '/' + item, 'r+') as file:
            data = json.load(file)
            data['image'] = newUrl + '/' + data['image'].split('/')[-1]
            file.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, file, indent=4)
            file.truncate()  # remove remaining part


newUrl = sys.argv[1]
path = sys.argv[2]
replace(newUrl, path)
