import json
import paho.mqtt.client as mqtt


class Subscriber:
    def __init__(self):
        self.broker = "mqtt.eclipseprojects.io"
        self.port = 1883
        self.client_id = "COMP-216-2024-GP2"
        self.callback_api_ver = mqtt.CallbackAPIVersion.VERSION2

    def create_client(self):
        self.client = mqtt.Client(callback_api_version=self.callback_api_ver)
        self.client.connect(self.broker, self.port)
        self.client.subscribe(self.client_id)
        self.client.on_message = self.on_message
        self.client.loop_forever()

    def on_message(self, msg):
        decoded_message = msg.payload.decode('utf-8')
        message_dict = json.loads(decoded_message)
        self.print_dictionary(message_dict)

    def print_dictionary(self, dictionary):
        print("id:", dictionary['id'])
        print("time:", dictionary['time'])
        print("temp:", dictionary['temp'])
        print("level:", dictionary['level'])


sub = Subscriber()
sub.create_client()