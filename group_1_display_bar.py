"""
COMP216 - Lab Assignment 7 & 8

Group: 1
Group Members:
    Handa, Karan
    Ngan, Tsang Kwong
    Patel, Jainam
    Wong, Yu Kwan
    ZHANG, AILIN

Date: March 10, 2024
"""

from tkinter import *
from tkinter import ttk
from collections import deque
import random
import time
import matplotlib.pyplot as plt

class TemperatureSensor:
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
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.data = deque(maxlen=60)

    def _generate_random_value(self):
        """
        Generates a random value between 0 and 1.

        Returns:
            float: A random value between 0 and 1.

        """
        return random.uniform(0, 1)

    @property
    def temperature(self):
        """
        Generates a random temperature value within the specified range.

        Returns:
            float: A random temperature value within the specified range.

        """
        normalized_value = self._generate_random_value()
        temperature = self.min_temp + (self.max_temp - self.min_temp) * normalized_value

        if len(self.data) == self.data.maxlen:
            self.data.popleft()

        self.data.append(temperature)

        return temperature


class TemperatureSensorApp:
    
    """
    A class representing a GUI application for temperature sensor display.

    Attributes:
        sensor (TemperatureSensor): The temperature sensor object.
        root (Tk): The main window of the application.
        value_label (Label): The label to display the sensor value.
        entry (Entry): The entry widget to input a new sensor value.
        update_button (Button): The button to update the sensor value.

    Methods:
        update_sensor_value: Updates the sensor value with the value from the entry widget.
        draw_line_graph: Draws a line graph of the temperature sensor data.
        run: Runs the Tkinter event loop.

    """

    def __init__(self, sensor):
        """
        Initializes a TemperatureSensorApp object.

        Args:
            sensor (TemperatureSensor): The temperature sensor object.

        """
        self.sensor = sensor
        self.current_temperture = sensor.temperature
        self.window_height = 800
        self.left_canvas_width = 400
        self.right_canvas_width = 800

        self.root = Tk()
        self.root.title("Temperature Sensor")
        self.root.configure(background="skyblue")

        self.main_frame = Frame(self.root)
        self.left_canvas = Canvas(self.main_frame, width=self.left_canvas_width, height=self.window_height, bg="white")
        self.right_canvas = Canvas(self.main_frame, width=self.right_canvas_width, height=self.window_height, bg="white")

        self.main_frame.pack()
        self.left_canvas.pack(side=LEFT)
        self.right_canvas.pack(side=RIGHT)

        self.current_temp_label = Label(self.left_canvas, text="Temperature: {:.2f} °C".format(self.current_temperture), font=("Arial", 20), bg="white")
        self.current_temp_label.pack(pady=20)

        self.input_field = Entry(self.left_canvas, font=("Arial", 20), bg="white")
        self.input_field.pack(pady=20)

        self.update_button = Button(self.left_canvas, text="Update", font=("Arial", 20), command=self.update_sensor_value, bg="white")
        self.update_button.pack(pady=20)

        # initialize the right canvas as a line graph
        self.draw_line_graph()


    def update_sensor_value(self):
        """
        Updates the sensor value with the value from the entry widget.

        """
        
        self.new_value = float(self.input_field.get())
        self.sensor.data.append(self.new_value)
        self.current_temperture = self.new_value
        self.current_temp_label.config(text="Temperature: {:.2f} °C".format(self.current_temperture))
        print(self.sensor.data)
        self.draw_line_graph()
    
    def draw_line_graph(self):
        """
        Draws a line graph of the temperature sensor data.

        """
        # Clear the canvas
        self.right_canvas.delete("all")
        x_scale = 40  # Scale for x-axis
        y_scale = 20  # Scale for y-axis
        x_offset = 30
        y_offset = 750

        x_values = range(len(self.sensor.data))

        # Draw x and y axes
        self.right_canvas.create_line(x_offset, y_offset, x_offset + (self.right_canvas_width - 50), y_offset, width=2)
        self.right_canvas.create_line(x_offset, y_offset, x_offset, y_offset - 700, width=2)
        
        # update the canvas with the new data
        for i in range(len(self.sensor.data) - 1):
            x1 = x_offset + i * x_scale
            y1 = y_offset - self.sensor.data[i] * y_scale
            x2 = x_offset + (i + 1) * x_scale
            y2 = y_offset - self.sensor.data[i + 1] * y_scale
            self.right_canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
            # Draw the data points
            self.right_canvas.create_oval(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill="blue")

        # Draw y-axis labels
        for i in range(0, 700, 100):
            self.right_canvas.create_text(x_offset - 10, y_offset - i * y_scale, text=str(i), anchor=E)

        
        # Draw the title
        self.right_canvas.create_text(self.right_canvas_width / 2, 20, text="Temperature Sensor Data", font=("Arial", 20))

        # Draw the x-axis label
        self.right_canvas.create_text(self.right_canvas_width / 2, 780, text="Time", font=("Arial", 12))

        # Draw the y-axis label
        self.right_canvas.create_text(20, 400, text="Temperature", font=("Arial", 12), angle=90)



    def run(self):
        """
        Runs the Tkinter event loop.

        """
        self.root.mainloop()



if __name__ == "__main__":
    sensor = TemperatureSensor()
    app = TemperatureSensorApp(sensor)
    app.run()
