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
<<<<<<< HEAD
    def __init__(self, min_temp=18, max_temp=23):
=======
    """
    A class representing a temperature sensor.

    Attributes:
        min_temp (float): The minimum temperature value.
        max_temp (float): The maximum temperature value.
        data (list): A list to store the generated temperature values.

    Methods:
        _generate_random_value: Generates a random value between 0 and 1.
        temperature: Generates a random temperature value within the specified range.

    """

    def __init__(self, min_temp=18, max_temp=23):
        """
        Initializes a TemperatureSensor object.

        Args:
            min_temp (float): The minimum temperature value (default: 18).
            max_temp (float): The maximum temperature value (default: 23).

        """
>>>>>>> 60afa274e2737568a0bb4a25cbe1543f7224e21e
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.data = []

    def _generate_random_value(self):
        """
        Generates a random value between 0 and 1.

        Returns:
            float: A random value between 0 and 1.

        """
        return random.uniform(0, 1)

    @property
    def temperature(self):
<<<<<<< HEAD
=======
        """
        Generates a random temperature value within the specified range.

        Returns:
            float: A random temperature value within the specified range.

        """
>>>>>>> 60afa274e2737568a0bb4a25cbe1543f7224e21e
        normalized_value = self._generate_random_value()
        temperature = self.min_temp + (self.max_temp - self.min_temp) * normalized_value
        self.data.append(temperature)
        return temperature

if __name__ == "__main__":
    sensor = TemperatureSensor()
    for i in range(10):
<<<<<<< HEAD
        print(sensor.temperature)
=======
        sensor.temperature
>>>>>>> 60afa274e2737568a0bb4a25cbe1543f7224e21e
    plt.plot(sensor.data)
    plt.title('Temperature Sensor')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.show()
    print(sensor.data)
<<<<<<< HEAD

=======
>>>>>>> 60afa274e2737568a0bb4a25cbe1543f7224e21e
