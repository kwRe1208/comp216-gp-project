"""
COMP216 - Lab Assignment 5

Group: 1
Group Members:
    Handa, Karan
    Ngan, Tsang Kwong
    Patel, Jainam
    Wong, Yu Kwan
    ZHANG, AILIN

Date: March 3, 2024
"""
import matplotlib.pyplot as plt
import random

class TemperatureSensor:
    def __init__(self, min_temp=18, max_temp=23):
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.data = []

    def _generate_random_value(self):
        return random.uniform(0, 1)

    @property
    def temperature(self):
        normalized_value = self._generate_random_value()
        temperature = self.min_temp + (self.max_temp - self.min_temp) * normalized_value
        self.data.append(temperature)
        return temperature

if __name__ == "__main__":
    sensor = TemperatureSensor()
    for i in range(10):
        print(sensor.temperature)
    plt.plot(sensor.data)
    plt.show()
    print(sensor.data)

