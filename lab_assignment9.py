"""
COMP216 - Lab Assignment 9

Group: 1
Group Members:
    Handa, Karan
    Ngan, Tsang Kwong
    Patel, Jainam
    Wong, Yu Kwan
    ZHANG, AILIN

Date: March 20, 2024
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

class DisplayChart:
    """
    A class representing a chart display (Line and Bar Chart for specified number of values). 
    
    Attributes:
        sensor (TemperatureSensor): A temperature sensor object.
    """
    def __init__(self, sensor):
        self.sensor = sensor
        self.data_list = []
        
        # Appending 20 values to the data_list which stays constant for the entire program
        for i in range(20):
            self.data_list.append(self.sensor.temperature)
    def on_go_button_click(self):
        # Error handling for invalid input
        try:
            data_points = int(self.input_field.get())
            self.draw_bar_line_chart(data_points)
        except ValueError:
            print("Invalid input")        
    
    def initUi(self):
        self.window_width = 800
        self.top_canvas_height = 100
        self.bottom_canvas_height = 400 

        self.root = Tk()
        self.root.title("Display Chart")
        self.main_frame = Frame(self.root)
        self.top_canvas = Canvas(self.main_frame,width=self.window_width, height=self.top_canvas_height, bg="white")
        self.bottom_canvas = Canvas(self.main_frame,width=self.window_width, height=self.bottom_canvas_height, bg="white")

        self.main_frame.pack()
        self.top_canvas.pack(side=TOP)
        self.bottom_canvas.pack(side=BOTTOM)
        
        self.data_label = Label(self.top_canvas, text="Data: ", font=("Arial", 12))
        self.data_label.pack(padx=5, pady=10)
        
        self.input_field = Entry(self.top_canvas, width=10)
        self.input_field.pack(padx=5, pady=10)        
        self.main_frame.pack()
        
        
        self.go_button = Button(self.top_canvas, text="Go", command=self.on_go_button_click)
        self.go_button.pack(padx=5, pady=10)      

        self.draw_bar_line_chart()
    
    def draw_bar_line_chart(self, data_points=0):
        """
        Draws a bar chart and line chart of the temperature sensor data.
        """
        
        self.bottom_canvas.delete("all" )
        # Line Chart 
        x_scale = 50  # Scale for x-axis
        y_scale = 5  # Scale for y-axis
        x_offset = 40
        y_offset = 350

        x_values = range(len(self.data_list))
        
        x_axis_length = self.window_width - 20  # Length of x-axis
        y_axis_length = 400  # Length of y-axis
        self.bottom_canvas.create_line(x_offset, y_offset, x_offset + (self.window_width - 50),y_offset, width=2)
        self.bottom_canvas.create_line(x_offset, y_offset, x_offset, y_offset - 300 , width=2)
        

        
        bar_width = 20
        gap = 10
        line_y_offset = 350
        
        
        bar_width = 20
        gap = 10
    # Draw bar chart
        for i in range(data_points):
            x1 = x_offset + i * x_scale
            y1 = y_offset
            x2 = x1 + x_scale
            y2 = y_offset - (self.data_list[i] * y_scale)
            self.bottom_canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
        for i in range(data_points ):
            x1 = x_offset + i * x_scale
            y1 = line_y_offset - self.data_list[i] * y_scale
            x2 = x_offset + (i + 1) * x_scale
            y2 = line_y_offset - self.data_list[i + 1] * y_scale
            self.bottom_canvas.create_line(x1, y1, x2, y2, fill="red", width=4)
            self.bottom_canvas.create_oval(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill="blue")
        for i in range(0, 400, 100):
            self.bottom_canvas.create_text(x_offset - 10, y_offset - i * y_scale, text=str(i), anchor=E)    
        # Draw the title
        self.bottom_canvas.create_text(self.bottom_canvas_height / 2, 20, text="Temperature Sensor Data", font=("Arial", 20))

        # Draw the x-axis label
        self.bottom_canvas.create_text(self.bottom_canvas_height / 2, 390, text="Time", font=("Arial", 12))

        # Draw the y-axis label
        self.bottom_canvas.create_text(20, 200, text="Temperature", font=("Arial", 12), angle=90)
        
    def run(self):
        """
        Runs the Tkinter event loop.

        """
        self.root.mainloop()

if __name__ == "__main__":
    sensor = TemperatureSensor()
    app = DisplayChart(sensor)
    app.initUi()
    app.run()
        
        