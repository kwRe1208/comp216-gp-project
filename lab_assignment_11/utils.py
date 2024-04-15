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
        
    def create_data(self) -> dict:
        #create and return a dict with the temperature data (randam float between 1 - 34)
        #make the temp to 1 decimal places
        self.start_id += 1
        self.temp = round(uniform(15, 24), 1)

        #Setup level of temperature based on the value
        if self.temp >= 15.0 and self.temp < 22.9:
            self.level = 'normal'
        elif self.temp >= 23.0 and self.temp <= 24.0:
            self.level = 'extreme'
        else:
            self.level = 'extreme'

        return {
            'id': self.start_id,
            'time': asctime(),
            'temp': self.temp,
            'level': self.level
        }
    
    def print_data(self):
        print(self.create_data())