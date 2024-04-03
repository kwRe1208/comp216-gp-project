#Import utils.py
from utils import Util
import paho.mqtt.client as mqtt
from random import uniform
import time
import json

class Publisher(Util):
    def __init__(self):
        super().__init__()
        self.broker = "mqtt.eclipseprojects.io"
        self.port = 1883
        self.callback_api_ver = mqtt.CallbackAPIVersion.VERSION2
        self.client_id = "COMP-216-2024-GP2"

    #convert the data get from Util to json format
    def convert_to_json(self):
        data = self.create_data()
        return json.dumps(data)

    #Create a mqtt client
    def create_client(self):
        self.client_pub = mqtt.Client(self.callback_api_ver, client_id=self.client_id)
        self.client_pub.connect(self.broker, self.port)
        self.client_pub.on_connect = self.on_connect
        print("Client created")
        self.client_pub.loop_start()
    
    #Connect to the server
    def on_connect(self, client, userdata, flags, reason, properties):
        print(f"Connected with reason code {reason}")

    #Publish the data to the server
    def publish_data(self):
        data = self.convert_to_json()
        self.client_pub.publish("TEMP-COMP216", data)
        self.on_publish(self.client_pub, data)
        

    def on_publish(self, client, userdata):
        print(client)
        print(userdata)
    
    def disconnect(self):
        self.client_pub.loop_stop()
        self.client_pub.disconnect()


pub = Publisher()
pub.create_client()

while True:
    pub.publish_data()
    time.sleep(2)

pub.disconnect()