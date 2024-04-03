# author : Narendra
# date   : November 22, 2021
#filename: wk12a_utils.py
#

#data format:
# id: 111
# time: 
# person: {
#  name: 'Narendra'
#  cell: '123-456-789'
# }
# core_temp: 98
# 
from random import uniform
from time import asctime
from json import dumps

class Util:
    def __init__(self):
        self.start_id = 100
        
    def create_data(self):
        #create and return a dict with the temperature data (randam float between 1 - 34)
        #make the temp to 1 decimal places
        self.start_id += 1
        self.temp = round(uniform(1, 34), 1)

        #Setup level of temperature based on the value
        if self.temp >= 1 and self.temp < 13:
            self.level = 'low'
        elif self.temp >= 13 and self.temp < 26:
            self.level = 'normal'
        elif self.temp >= 26 and self.temp < 30:
            self.level = 'high'
        else:
            self.level = 'extreme'

        data = {
            'id': self.start_id,
            'time': asctime(),
            'temp': self.temp,
            'level': self.level
        }

        return data
    
    def print_data(self):
        print(self.create_data())