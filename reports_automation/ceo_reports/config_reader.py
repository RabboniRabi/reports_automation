"""
Module with functions to read the configurations given for each report in JSON format
"""

import json

with open('report_configs.json' , 'r') as read_file:
    config = json.load(read_file)



print('config type: ' , type(config))

print(config)