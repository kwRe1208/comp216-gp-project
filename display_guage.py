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

import colorsys
import math
from tkinter import *
from PIL import ImageColor


class DisplayGauge:
    """
    A class representing a display gauge.
    """
    _OUTER_FRAME_COLOR = "#303030"
    _INNER_FRAME_COLOR = "#a0a0a0"
    _BACKGROUND_COLOR = "#f0f0f0"
    _NEEDLE_COLOR = "#303030"
    _NEDDLE_WIDTH = 3
    _MARK_COLOR = "#303030"
    _MARK_SIZE = 10
    _MARK_WIDTH = 1
    _MAJOR_MARK_COLOR = "#303030"

    _DEFAULT_VALUE = 0
    _DEFAULT_VALUE_UNIT = "°C"
    _DEFAULT_MIN_VALUE = 0
    _DEFAULT_MAX_VALUE = 120
    _DEFAULT_ANGLE_RANGE = 240
    _DEFAULT_MARK_INTERVAL = 1
    _DEFAULT_MAJOR_MARK_COUNT = 5
    _DEFAULT_LABEL_MARK_COUNT = _DEFAULT_MAJOR_MARK_COUNT * 2

    _DEFAULT_COLOR_START = "#00ff00"
    _DEFAULT_COLOR_END = "#ff0000"

    _WIDTH = 400  # cannot be changed
    _HEIGHT = 400 # cannot be changed

    def __init__(self, root,
            value: float = _DEFAULT_VALUE,
            min_value: float = _DEFAULT_MIN_VALUE,
            max_value: float = _DEFAULT_MAX_VALUE,
            value_unit: str = _DEFAULT_VALUE_UNIT,
            angle_range: int = _DEFAULT_ANGLE_RANGE,
            mark_interval: float = _DEFAULT_MARK_INTERVAL,
            major_mark_steps: int = _DEFAULT_MAJOR_MARK_COUNT,
            label_mark_steps: int = _DEFAULT_LABEL_MARK_COUNT,
            color_start: str = _DEFAULT_COLOR_START,
            color_end: str = _DEFAULT_COLOR_END):
        """
        Initializes a DisplayGauge object.
        Parameters:
            root (Tk): The root window of the application.
            value (float): The initial value of the gauge (default: 0).
            min_value (float): The minimum value of the gauge (default: 0).
            max_value (float): The maximum value of the gauge (default: 120).
            value_unit (str): The unit of the value (default: "°C").
            angle_range (int): The angle range of the gauge (default: 240).
            mark_interval (float): The interval between marks (default: 1).
            major_mark_steps (int): The number of major marks (default: 5).
            label_mark_steps (int): The number of label marks (default: 10).
            color_start (str): The start color of the gauge (default: "#00ff00").
            color_end (str): The end color of the gauge (default: "#ff0000").
        """
        self._root = root
        self._root.geometry(f"{DisplayGauge._WIDTH}x{DisplayGauge._HEIGHT}")
        self._value = value
        self._value_unit = value_unit
        self._min_value = min_value
        self._max_value = max_value
        self._angle_range = angle_range
        self._angle_start = angle_range / 2 + 90 # 90 degree offset
        self._mark_interval = mark_interval
        self._major_mark_steps = major_mark_steps
        self._label_mark_steps = label_mark_steps
        self._color_start = color_start
        self._color_end = color_end
        self._color_start_hsb = colorsys.rgb_to_hsv(*ImageColor.getrgb(color_start))
        self._color_end_hsb = colorsys.rgb_to_hsv(*ImageColor.getrgb(color_end))
        self._canvas = Canvas(self._root, width=DisplayGauge._WIDTH, height=DisplayGauge._HEIGHT)
        self._dynamic_objects = []
        self._canvas.pack()
        self._draw_guage()

    @property
    def value(self):
        """ Returns the current value of the gauge. """
        return self._value

    @value.setter
    def value(self, value: float):
        """ Sets the current value of the gauge. The gauge will be updated accordingly."""
        self._clear_dynamic_objects()
        self._value = value
        self._draw_needle()
        self._draw_value()

    @property
    def min_value(self):
        """ Returns the minimum value of the gauge."""
        return self._min_value

    @property
    def max_value(self):
        """ Returns the maximum value of the gauge."""
        return self._max_value

    @property
    def angle_range(self):
        """ Returns the angle range of the gauge."""
        return self._angle_range

    @property
    def mark_interval(self):
        """ Returns the interval between marks of the gauge."""
        return self._mark_interval

    @property
    def major_mark_steps(self):
        """ Returns the number of marks for a major mark of the gauge."""
        return self._major_mark_steps

    @property
    def label_mark_steps(self):
        """ Returns the number of marks for a label mark of the gauge."""
        return self._label_mark_steps

    @property
    def color_start(self):
        """ Returns the start color of the gauge."""
        return self._color_start

    @property
    def color_end(self):
        """ Returns the end color of the gauge."""
        return self._color_end

    def _draw_guage(self):
        """ Draws the gauge. """
        self._draw_shape()
        self._draw_cirular_ruler()
        self._draw_needle()
        self._draw_value()

    def _draw_shape(self):
        """ Draws the shape of the gauge. """
        self._canvas.create_oval(
            40, 40, 360, 360,
            fill=DisplayGauge._BACKGROUND_COLOR,
            outline=DisplayGauge._OUTER_FRAME_COLOR, width=15
        ),
        self._canvas.create_oval(
            45, 45, 355, 355,
            fill=DisplayGauge._BACKGROUND_COLOR,
            outline=DisplayGauge._INNER_FRAME_COLOR, width=5
        )
        self._canvas.create_oval(
            190, 190, 210, 210,
            fill=DisplayGauge._NEEDLE_COLOR,
            outline=DisplayGauge._NEEDLE_COLOR
        ),

    def _draw_cirular_ruler(self):
        """ Draws the circular ruler of the gauge. """
        self._draw_circular_ruler_hue()
        self._draw_circular_ruler_marks()

    def _draw_circular_ruler_hue(self):
        """ Draws the hue of the circular ruler of the gauge. """
        for angle in range(0, self._angle_range + 1, 1):
            color = self._convert_angle_to_color(angle)
            self._canvas.create_arc(80, 80, 320, 320,
                start=self._angle_start - angle, extent=1,
                fill=color, outline=color, width=40, style=ARC
            )

    def _draw_circular_ruler_marks(self):
        """ Draws the marks of the circular ruler of the gauge."""
        steps = int((self._max_value - self._min_value) / self._mark_interval)
        for step in range(0, steps + 1, 1):
            value = self._min_value + step * self._mark_interval
            angle = self._convert_value_to_angle(value)
            angle_actual = self._angle_start - angle
            mark_size = DisplayGauge._MARK_SIZE
            mark_start = 100
            mark_end = 300
            mark_color = DisplayGauge._MARK_COLOR

            # Draw the label marks
            if step % self._label_mark_steps == 0:
                radius = (mark_end - mark_start) / 2 - 20
                y = radius * math.sin(math.radians(angle_actual))
                x = radius * math.cos(math.radians(angle_actual))
                self._canvas.create_text(200+x, 200-y, text=f"{value}", font=("Arial", 10))

            # Draw the major marks
            if step % self._major_mark_steps == 0:
                mark_size += 10
                mark_start -= 5
                mark_end += 5
                mark_color = DisplayGauge._MAJOR_MARK_COLOR

            # Draw the marks
            self._canvas.create_arc(
                mark_start, mark_start, mark_end, mark_end,
                start=angle_actual, extent=0.5,
                fill=mark_color,
                outline=mark_color, width=mark_size, style=ARC
            )

    def _draw_needle(self):
        """ Draws the needle of the gauge. """
        angle = self._angle_start - self._convert_value_to_angle(self._value)
        self._add_dynamic_objects(
            self._canvas.create_arc(
                115, 115, 285, 285,
                start=angle-0.5, extent=1, width=DisplayGauge._NEDDLE_WIDTH,
                fill=DisplayGauge._NEEDLE_COLOR,
                outline = DisplayGauge._NEEDLE_COLOR,
                style=PIESLICE
            )
        )

    def _draw_value(self):
        """ Draws the value of the gauge. """
        self._add_dynamic_objects(
            self._canvas.create_text(200, 275, text=f"{self._value} {self._value_unit}", font=("Arial", 24))
        )

    def _add_dynamic_objects(self, *objects):
        self._dynamic_objects.extend(objects)

    def _clear_dynamic_objects(self):
        self._canvas.delete(*self._dynamic_objects)
        self._dynamic_objects = []

    def _convert_value_to_angle(self, value: float) -> float:
        return (value - self._min_value) / (self._max_value - self._min_value) * self._angle_range

    def _convert_angle_to_color(self, angle: float) -> str:
        ratio = angle / self._angle_range
        hsv_start = self._color_start_hsb
        hsv_end = self._color_end_hsb
        h = (hsv_end[0] - hsv_start[0]) * ratio + hsv_start[0]
        s = (hsv_end[1] - hsv_start[1]) * ratio + hsv_start[1]
        v = (hsv_end[2] - hsv_start[2]) * ratio + hsv_start[2]
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return f"#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}"


if __name__ == "__main__":
    root = Tk()
    display_gauge = DisplayGauge(root, value=0, min_value=-20, max_value=100, value_unit="°C")
    value = display_gauge.min_value
    while value <= display_gauge.max_value:
        display_gauge.value = value
        root.update()
        root.after(1000)
        value += display_gauge.mark_interval

    root.mainloop()
