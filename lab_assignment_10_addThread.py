"""
COMP216 - Lab Assignment 9

Group: 1
Group Members:
    Handa, Karan
    Ngan, Tsang Kwong
    Patel, Jainam
    Wong, Yu Kwan
    ZHANG, AILIN

Date: March 30, 2024
"""
from random import random
from tkinter import Canvas, Frame, Label, Button, Tk, messagebox, Spinbox, Widget
import threading
import time

class DisplayChart(Widget):
    """
    DisplayChart class for displaying historical data in a chart.
    """

    _WIDTH = 600    # Default width of the chart
    _HEIGHT = 400   # Default height of the chart

    def __init__(
            self, master,
            width: int = _WIDTH,
            height: int = _HEIGHT,
            bg: str = "white",
            color: str = "blue",
            x_step: float = 80,
            x_offset: float = 125,
            y_offset: float = 60,
            value_min: float = 0,
            value_max: float = 800,
            value_scale: float = None):
        """
        Create a new DisplayChart object.
        :param master: The parent widget.
        :param width: The width of the chart in pixels.
        :param height: The height of the chart in pixels.
        :param bg: The background color of the chart.
        :param color: The color of the chart elements.
        :param x_step: The horizontal step size between data points.
        :param x_offset: The horizontal offset of the chart.
        :param y_offset: The vertical offset of the chart.
        :param value_min: The minimum value of the y-axis.
        :param value_max: The maximum value of the y-axis.
        :param value_scale: The scale factor for the y-axis.
        """
        Widget.__init__(self, master, 'frame')
        self._width = width
        self._height = height
        self._bg = bg
        self._color = color
        self._x_step = x_step
        self._x_offset = x_offset
        self._y_offset = y_offset
        self._value_min = value_min
        self._value_max = value_max
        self._value_scale = value_scale or (self._height - self._y_offset) / (value_max - value_min)
        self._canvas = Canvas(self, width=width, height=height, bg=bg, bd=1, relief="ridge")
        self._canvas.pack()
        self._series_list = []
        self._x_axis_objects = []
        self._y_axis_objects = []

    @property
    def canvas(self) -> Canvas:
        """Return the canvas object."""
        return self._canvas

    class Series:
        """Series class for managing chart series."""
        def __init__(self, canvas: Canvas, objects: list[int]):
            """
            Create a new Series object.
            :param canvas:
            :param objects:
            """
            self._canvas = canvas
            self._objects = objects

        def hide(self):
            """Hide the series."""
            for obj in self._objects:
                self._canvas.itemconfig(obj, state="hidden")

        def show(self, on: bool = True):
            """Show or hide the series."""
            for obj in self._objects:
                self._canvas.itemconfig(obj, state="normal" if on else "hidden")

        def delete(self):
            """Delete the series."""
            for obj in self._objects:
                self._canvas.delete(obj)

    def _translate_x(self, x: float) -> float:
        return self._x_offset + x

    def _translate_y(self, value: float) -> float:
        return self._height - self._y_offset - (value - self._value_min) * self._value_scale

    def _translate_point(self, x: float, value: float) -> (float, float):
        return self._translate_x(x), self._translate_y(value)

    def clear_x_axis(self):
        """Clear the x-axis."""
        for obj in self._x_axis_objects:
            self._canvas.delete(obj)
        self._x_axis_objects.clear()

    def clear_y_axis(self):
        """Clear the y-axis."""
        for obj in self._y_axis_objects:
            self._canvas.delete(obj)
        self._y_axis_objects.clear()

    # def draw_bars(
    #         self,
    #         data: list[float],
    #         color: str = None,
    #         width: float = None) -> Series:
    #     """
    #     Draw a series of bars.
    #     :param data: The data points.
    #     :param color: The color of the bars.
    #     :param width: The width of the bars.
    #     :return: The series object.
    #     """
    #     color = color or self._color
    #     width = width or self._x_step * 0.75
    #     if width <= 0 or width >= self._x_step:
    #         raise ValueError("Invalid width")
    #     objects = []
    #     for i in range(len(data)):
    #         x = i * self._x_step
    #         x0, y0 = self._translate_point(x - width / 2, 0)
    #         x1, y1 = self._translate_point(x + width / 2, data[i])
    #         objects.append(self._canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color))
    #     series = DisplayChart.Series(self._canvas, objects)
    #     self._series_list.append(series)
    #     return series

    def draw_points(
            self,
            data: list[float],
            color: str = None,
            fill: bool = True,
            size: float = 10,
            shape: str = "circle") -> Series:
        """
        Draw a series of points.
        :param data: The data points.
        :param color: The color of the points.
        :param fill: Fill the points.
        :param size: The size of the points.
        :param shape: The shape of the points.
        :return: The series object.
        """
        if (size <= 0) or (shape not in ["circle", "square", "triangle"]):
            raise ValueError("Invalid size or shape")
        color = color or self._color
        fill_color = color if fill else "white"
        prev_x: float = 0
        prev_y: float = 0
        objects = []
        for i in range(len(data)):
            x, y = self._translate_point(i * self._x_step, data[i])
            if shape == "circle":
                r = size / 2
                objects.append(
                    self._canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill_color, outline=color, width=1))
            elif shape == "square":
                d = size / 2
                objects.append(
                    self._canvas.create_rectangle(x - d, y - d, x + d, y + d, fill=fill_color, outline=color, width=1))
            elif shape == "triangle":
                dx = size / 2
                dy = size / 2
                triangle = [x, y - dy, x - dx, y + dy, x + dx, y + dy]
                objects.append(
                    self._canvas.create_polygon(triangle, fill=fill_color, outline=color, width=1))
            else:
                raise ValueError(f"Invalid shape: {shape}")
        series = DisplayChart.Series(self._canvas, objects)
        self._series_list.append(series)
        return series

    def draw_lines(
            self,
            data: list[float],
            color: str = None,
            width: float = 2,
            shape: str = "solid") -> Series:
        """
        Draw a series of lines.
        :param data: The data points.
        :param color: The color of the lines.
        :param width: The width of the lines.
        :param shape: The shape of the lines.
        :return: The series object.
        """
        if (width <= 0) or (shape not in ["solid", "dotted", "dashed"]):
            raise ValueError("Invalid width or shape")
        color = color or self._color
        prev_x, prev_y = self._translate_point(0, data[0])
        objects = []
        for i in range(1, len(data)):
            x, y = self._translate_point(i * self._x_step, data[i])
            if shape == "solid":
                objects.append(self._canvas.create_line(prev_x, prev_y, x, y, fill=color, width=width))
            elif shape == "dotted":
                objects.append(self._canvas.create_line(prev_x, prev_y, x, y, fill=color, width=width, dash=(2, 2)))
            elif shape == "dashed":
                objects.append(self._canvas.create_line(prev_x, prev_y, x, y, fill=color, width=width, dash=(8, 4)))
            else:
                raise ValueError(f"Invalid shape: {shape}")
            prev_x = x
            prev_y = y
        series = DisplayChart.Series(self._canvas, objects)
        self._series_list.append(series)
        return series

    def draw_x_axis(self, title: str, labels: list[str]):
        """
        Draw the x-axis.
        :param title: The title of the x-axis.
        :param labels: The labels of the x-axis.
        """
        self.clear_x_axis()
        x0, y0 = self._translate_point(0, self._value_min)
        self._x_axis_objects.append(
            self._canvas.create_rectangle(0, y0, self._width, self._height + 100, fill=self._bg, outline=self._bg)
        )
        self._x_axis_objects.append(
            self._canvas.create_text(self._width / 2, y0 + 42, text=title, anchor="center"))
        for i in range(len(labels)):
            x = self._translate_x(i * self._x_step)
            self._x_axis_objects.append(self._canvas.create_text(x, y0 + 16, text=labels[i], anchor="n"))

    def draw_y_axis(self, title: str, value_step: float, unit: str = ""):
        """
        Draw the y-axis.
        :param title: The title of the y-axis.
        :param value_step: The step size of the y-axis.
        :param unit: The unit of the y-axis.
        """
        if value_step <= 0:
            raise ValueError("Invalid value step")
        self.clear_y_axis()
        steps = int((self._value_max - self._value_min) / value_step)
        x0 = self._translate_x(0)
        self._y_axis_objects.append(
            self._canvas.create_text(x0 - self._x_offset + 18, self._height / 2, text=title, anchor="center", angle=90))
        for i in range(steps):
            value = i * value_step + self._value_min
            label = str(value) + unit
            y = self._translate_y(value)
            self._y_axis_objects.append(self._canvas.create_text(x0 - 50, y, text=label, anchor="e"))

    def clear(self):
        """Clear the chart."""
        self.clear_x_axis()
        self.clear_y_axis()
        for series in self._series_list:
            series.delete()
        self._series_list.clear()


class DisplayChartApp:
    """DisplayChartApp class for displaying historical data in a chart application."""
    def __init__(
            self,
            root: Tk,
            data_points: list[float],
            value_min: float,
            value_max: float,
            value_unit: str,
            x_axis_title: str,
            y_axis_title: str,
            y_axis_step: float,
            items_per_page: int = 6,
            width: int = 600,
            height: int = 400,
            title: str = "Dynamic Chart"):
        """
        Create a new DisplayChartApp object.
        :param root: The root window.
        :param data_points: The data points.
        :param value_min: The minimum value of the y-axis.
        :param value_max: The maximum value of the y-axis.
        :param value_unit: The unit of the y-axis.
        :param x_axis_title: The title of the x-axis.
        :param y_axis_title: The title of the y-axis.
        :param y_axis_step: The step size of the y-axis.
        :param items_per_page: The number of items per page.
        :param width: The width of the chart in pixels.
        :param height: The height of the chart in pixels.
        :param title: The title of the application.
        """
        self._root = root
        self._root.title(title)
        self._root.geometry(f"{width + 40}x{height + 80}")
        self._data_points = data_points
        self._value_min = value_min
        self._value_max = value_max
        self._value_unit = value_unit
        self._x_axis_title = x_axis_title
        self._y_axis_title = y_axis_title
        self._y_axis_step = y_axis_step
        self._items_per_page = items_per_page
        self._frame = Frame(self._root)
        self._frame.columnconfigure(0, weight=0, pad=2)
        self._frame.columnconfigure(1, weight=0, pad=2)
        self._frame.columnconfigure(2, weight=1, pad=2)
        self._frame.rowconfigure(0, weight=1, pad=20)
        self._frame.rowconfigure(1, weight=1)

        self._button = Button(
            self._frame,
            text="Start / Pause",
            width=15,
            font=("Arial", 12),
            command=self._draw_chart_on_input
        )
        self._button.grid(row=0, column=2, sticky="w")
        self._chart = DisplayChart(
            self._frame,
            width, height,
            value_min=value_min,
            value_max=value_max,
        )
        self._chart.grid(row=1, column=0, columnspan=3)
        self._frame.pack()
        
        
        # Remove the Entry widget
        self._button.destroy()

        # Create a thread and set the target to the method
        self._thread = threading.Thread(target=self._update_data_and_draw_chart)
        self._thread.daemon = True  # Terminate the thread when the GUI closes
        self._thread.start()

    def draw_chart(self, start_index: int = 0, end_index: int = None):
        """
        Draw the chart.
        :param start_index: The start index of the data points.
        :param end_index: The end index of the data points.
        """
        end_index = end_index or min(len(self._data_points), start_index + self._items_per_page)
        self._chart.clear()
        self._chart.draw_lines(self._data_points[start_index:end_index], color="red")
        self._chart.draw_x_axis(self._x_axis_title, [str(i) for i in range(start_index, end_index)])
        self._chart.draw_y_axis(self._y_axis_title, self._y_axis_step, self._value_unit)

    def _draw_chart_on_input(self):
        try:
            start_index = 0
            if (start_index < 0) or (start_index >= len(self._data_points)):
                raise ValueError("Invalid Input!\nIndex value must be >= 0 and <" + str(len(self._data_points)))
            self.draw_chart(start_index)
        except ValueError as e:
            messagebox.showerror('Input Error', str(e))

    def _validate_on_input(self, value: str) -> bool:
        if str.isdigit(value) or value == "":
            return True
        else:
            return False
        
    def _update_data_and_draw_chart(self):
        while True:
            # Remove the first item in the list of values
            self._data_points.pop(0)
            # Add a new random value to the end of the list
            self._data_points.append(random() * 8 + 16)
            # Call the method to display list on the canvas
            self.draw_chart()
            # Sleep for a short while (0.5 of a second)
            time.sleep(0.5)


#
# Main function for testing the DisplayChartApp class
# Usage: python DisplayChart.py
#
if __name__ == "__main__":
    root = Tk()
    data_points = [random() * 8 + 16 for _ in range(100)]
    app = DisplayChartApp(
        root,
        data_points,
        value_min=15,
        value_max=25,
        value_unit="°C",
        x_axis_title="Time",
        y_axis_title="Temperature",
        y_axis_step=1
    )
    root.mainloop()
