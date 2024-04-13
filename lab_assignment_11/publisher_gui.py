import tkinter as tk
from Wk12a_publisher import Publisher   # Import your Publisher class from publisher.py
import threading   # Import the threading module to handle continuous publishing
import time
from tkinter import ttk
import json

class PublisherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Publisher")

        self.publisher = Publisher()  # Initialize an instance of your Publisher class
        self.data_table = None

        self.create_widgets()

    def create_widgets(self):
        # Create a frame for organizing widgets
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        # Label for showing status
        self.status_label = tk.Label(self.frame, text="Status: Idle", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Button to start publishing
        self.start_button = tk.Button(self.frame, text="Start Publishing", command=self.start_publishing)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Button to stop publishing
        self.stop_button = tk.Button(self.frame, text="Stop Publishing", command=self.stop_publishing, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Create a table to display data
        self.create_table()

    def create_table(self):
        self.data_table = ttk.Treeview(self.root, columns=("ID", "Time", "Temperature", "Level"), show="headings")
        self.data_table.heading("ID", text="ID")
        self.data_table.heading("Time", text="Time")
        self.data_table.heading("Temperature", text="Temperature")
        self.data_table.heading("Level", text="Level")
        self.data_table.pack(padx=10, pady=10)

    def start_publishing(self):
        self.publisher.create_client()
        self.status_label.config(text="Status: Publishing", bg="green")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Set the flag to indicate that publishing is ongoing
        self.publishing_flag = True
        
        # Start a new thread for continuous publishing
        self.publish_thread = threading.Thread(target=self.continuous_publishing)
        self.publish_thread.start()
        
    def continuous_publishing(self):
        while getattr(self, "publishing_flag", True):
            data = self.publisher.convert_to_json()
            self.publisher.publish_data()
            self.display_data(data)
            time.sleep(2)  # Adjust the sleep duration as needed
            
    def stop_publishing(self):
        # Set the flag to stop publishing
        self.publishing_flag = False
        
        # Disconnect the publisher
        self.publisher.disconnect()
        
        self.status_label.config(text="Status: Idle", bg="red")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def display_data(self, data):
        # Parse JSON data
        data_dict = json.loads(data)
        
        # Insert data into table
        self.data_table.insert("", "end", values=(data_dict["id"], data_dict["time"], data_dict["temp"], data_dict["level"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = PublisherGUI(root)
    root.mainloop()
