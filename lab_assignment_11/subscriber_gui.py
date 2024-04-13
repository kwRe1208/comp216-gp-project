import threading
import time
import tkinter as tk
from tkinter import ttk
import json
import paho.mqtt.client as mqtt
from Wk12a_subscriber import Subscriber


class SubscriberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Subscriber")

        self.subscriber = Subscriber()  # Initialize an instance of your Subscriber class
        self.create_widgets()
        self.subscriber_thread_started = False  # Flag to track whether subscriber thread has started

    def create_widgets(self):
        # Create a frame for organizing widgets
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        # Label for displaying received data
        self.data_label = tk.Label(self.frame, text="Received Data:", font=("Arial", 12))
        self.data_label.pack()

        # Create a treeview widget to display data in tabular format
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Time", "Temperature", "Level"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Temperature", text="Temperature")
        self.tree.heading("Level", text="Level")
        self.tree.pack()

        # Button to start subscribing
        self.start_button = tk.Button(self.frame, text="Start Subscribing", command=self.start_subscribing)
        self.start_button.pack(pady=10)

        # Button to stop subscribing
        self.stop_button = tk.Button(self.frame, text="Stop Subscribing", command=self.stop_subscribing, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

    def start_subscribing(self):
        if not self.subscriber_thread_started:  # Check if subscriber thread has started
            self.subscriber.create_client()  # Create MQTT client
            self.subscriber.start_subscriber_thread()
            self.subscriber_thread_started = True
            self.start_button.config(state=tk.DISABLED)  # Disable start button
            self.stop_button.config(state=tk.NORMAL)    # Enable stop button

    def stop_subscribing(self):
        self.subscriber.stop_subscriber_thread()  # Stop the subscriber thread
        self.start_button.config(state=tk.NORMAL)  # Enable start button
        self.stop_button.config(state=tk.DISABLED) # Disable stop button
        self.subscriber_thread_started = False

    def update_data_display(self):
        # Periodically check for new data and update the display
        threading.Thread(target=self._update_data_display_thread, daemon=True).start()

    def _update_data_display_thread(self):
        while True:
            if self.subscriber_thread_started and self.subscriber.data_points:  # Check if subscriber thread has started and there is new data available
                data_dict = {
                    "id": self.subscriber.data_ids[0],
                    "time": time.strftime("%a %b %d %H:%M:%S %Y"),
                    "temp": self.subscriber.data_points[0],
                    "level": self.subscriber.data_level[0]
                }
                self.display_data(data_dict)
                self.subscriber.data_ids.pop(0)
                self.subscriber.data_points.pop(0)
                self.subscriber.data_level.pop(0)
            time.sleep(1)  # Check for new data every 1 second

    def display_data(self, data_dict):
        """ 
        Display received data in the GUI.

        Args:
            data_dict (dict): The dictionary containing the received data.
        """
        self.tree.insert("", tk.END, values=(data_dict["id"], data_dict["time"], data_dict["temp"], data_dict["level"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = SubscriberGUI(root)
    app.update_data_display()  # Start the data display update loop
    root.mainloop()
