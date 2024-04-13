"""
COMP216 - Lab Assignment 11 - Publisher

Group: 1
Group Members:
    Handa, Karan
    Ngan, Tsang Kwong
    Patel, Jainam
    Wong, Yu Kwan
    ZHANG, AILIN

Date: April 6, 2024
"""

#Import utils.py
from utils import Util
import paho.mqtt.client as mqtt
from random import uniform
import time
import json


class Publisher(Util):
    """
    A class representing a publisher that publishes data to an MQTT server.

    Attributes:
        broker (str): The MQTT broker address.
        port (int): The MQTT broker port.
        callback_api_ver (int): The MQTT callback API version.
        client_id (str): The client ID for the MQTT client.
        topic (str): The topic to publish the data to.
        client_pub (mqtt.Client): The MQTT client instance.

    Methods:
        convert_to_json: Converts the data obtained from Util to JSON format.
        create_client: Creates an MQTT client and connects to the broker.
        on_connect: Callback function called when the client connects to the broker.
        publish_data: Publishes the data to the MQTT server.
        on_publish: Callback function called after publishing data.
        disconnect: Disconnects the MQTT client from the broker.
    """

    def __init__(self):
        super().__init__()
        self.broker = "mqtt.eclipseprojects.io"
        self.port = 1883
        self.callback_api_ver = mqtt.CallbackAPIVersion.VERSION2
        self.client_id = "COMP216-2024-GP1"
        self.topic = "TEMP-COMP216-GP1"

    def convert_to_json(self):
        """
        Converts the data obtained from Util to JSON format.

        Returns:
            str: The JSON representation of the data.
        """
        data = self.create_data()
        return json.dumps(data)

    def create_client(self):
        """
        Creates an MQTT client and connects to the broker.

        Raises:
            TimeoutError: If the connection to the broker times out.
        """
        try:
            self.client_pub = mqtt.Client(self.callback_api_ver, client_id=self.client_id)
            self.client_pub.connect(self.broker, self.port)
            self.client_pub.on_connect = self.on_connect
            print("Client created")
            self.client_pub.loop_start()
        except TimeoutError:
            raise TimeoutError("Connection timeout")

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

    def publish_data(self):
        """
        Publishes the data to the MQTT server.
        """
        data = self.convert_to_json()
        try:
            self.client_pub.publish(self.topic, data)
            self.on_publish(self.client_pub, data)
        except Exception as e:
            raise e

    def on_publish(self, client, userdata):
        """
        Callback function called after publishing data.

        Args:
            client (mqtt.Client): The MQTT client instance.
            userdata: The user data associated with the client.
        """
        print(client)
        print(userdata)

    def disconnect(self):
        """
        Disconnects the MQTT client from the broker.
        """
        self.client_pub.loop_stop()
        self.client_pub.disconnect()



if __name__ == "__main__":
    pub = Publisher()
    pub.create_client()
    while True:
        pub.publish_data()
        time.sleep(2)

#pub.disconnect()