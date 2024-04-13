"""
COMP216 - Lab Assignment 11 - Subscriber

Group: 1
Group Members:
    Handa, Karan
    Ngan, Tsang Kwong
    Patel, Jainam
    Wong, Yu Kwan
    ZHANG, AILIN

Date: April 6, 2024
"""

import json
import paho.mqtt.client as mqtt
import threading

class Subscriber:
    """
    A class representing an MQTT subscriber.

    Attributes:
        broker (str): The MQTT broker to connect to.
        port (int): The port number of the MQTT broker.
        client_id (str): The client ID for the MQTT connection.
        callback_api_ver (int): The version of the MQTT callback API to use.
        topic (str): The topic to subscribe to.

    Methods:
        create_client: Creates an MQTT client and connects to the broker.
        on_connect: Callback function called when the client connects to the broker.
        on_message: Callback function called when a message is received.
        print_dictionary: Prints the contents of a dictionary.
        disconnect: Disconnects the MQTT client from the broker.
    """

    def __init__(self):
        self.broker = "mqtt.eclipseprojects.io"
        self.port = 1883
        self.client_id = "COMP216-2024-GP1"
        self.callback_api_ver = mqtt.CallbackAPIVersion.VERSION2
        self.topic = "TEMP-COMP216-GP1"
        self.data_points = []
        self.data_ids = []
        self.data_level = []

    def create_client(self):
        """
        Creates an MQTT client and connects to the broker.
        """
        try:
            self.client = mqtt.Client(callback_api_version=self.callback_api_ver)
            self.client.connect(self.broker, self.port)
            self.client.on_connect = self.on_connect
            self.client.subscribe(self.topic)
            self.client.on_message = self.on_message
        except TimeoutError:
            print("Connection to the broker timed out")

    def start_subscriber_thread(self):
        # Start a new thread for the subscriber
        self.subscriber_thread = threading.Thread(target=self.client.loop_forever, kwargs={"retry_first_connection": True})
        self.subscriber_thread.daemon = True  # Set the thread as a daemon so it terminates with the main thread
        self.subscriber_thread.start()

    def stop_subscriber_thread(self):
        # Disconnect the client and stop the thread
        self.client.disconnect()
        self.subscriber_thread.join()  # Wait for the thread to terminate

    
    def on_connect(self, client, userdata, flags, reason, properties):
        """
        Callback function called when the client connects to the broker.

        Args:
            client (mqtt.Client): The MQTT client instance.
            userdata: The user data associated with the client.
            flags: The flags associated with the connection.
            reason (int): The reason code for the connection.
            properties: The properties associated with the connection.
        """
        print("Connected with result code {0}".format(str(reason)))
        print("Subscribing to topic:", self.topic)
        print("Waiting for messages...")

    def on_message(self, client, userdata, msg):
        """
        Callback function called when a message is received.

        Args:
            client (mqtt.Client): The MQTT client instance.
            userdata: The user data associated with the client.
            msg (mqtt.MQTTMessage): The received message.
        """
        decoded_message = msg.payload.decode('utf-8')
        message_dict = json.loads(decoded_message)
        self.print_dictionary(message_dict)
        self.store_data(message_dict)

    def store_data(self, dictionary):
        """
        Stores the received data in a list.

        Args:
            dictionary (dict): The dictionary containing the data.
        """
        queue_length = 5
        if len(self.data_points) == queue_length:
            self.data_points.pop(0)
            self.data_ids.pop(0)

        self.data_points.append(dictionary['temp'])
        self.data_ids.append(dictionary['id'])
        self.data_level.append(dictionary['level'])
        print(self.data_ids, self.data_points)

    def print_dictionary(self, dictionary):
        """
        Prints the contents of a dictionary.

        Args:
            dictionary (dict): The dictionary to print.
        """
        print("id:", dictionary['id'])
        print("time:", dictionary['time'])
        print("temp:", dictionary['temp'])
        print("level:", dictionary['level'])
    
    def unsubscribe(self):
        """
        Unsubscribes from the topic.
        """
        self.client.unsubscribe(self.topic)

    def disconnect(self):
        """
        Disconnects the MQTT client from the broker.
        """
        self.client.loop_stop()
        self.client.disconnect()

if __name__ == "__main__":
    sub = Subscriber()
    sub.create_client()
