#Build mqtt client to send data to the broker

import paho.mqtt.client as mqtt
from random import uniform
import time

# Define parameter variables
broker = "mqtt.eclipseprojects.io"
port = 1883


def on_connect(client, userdata, flags, reason, properties):
    print(f"Connected with reason code {reason}")

def on_publish(client, userdata, mid, reason, properties):
    print(client)
    print(userdata)
    print(mid)
    print(reason)


client_pub = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="COMP-216-2024")
client_pub.on_connect = on_connect
client_pub.connect(broker, port)

client_pub.loop_start()

for i in range(7):
    random_value = uniform(10.0, 32.0)
    client_pub.publish("TEMP-COMP216", random_value)
    print(f"Published: {random_value} to Topic TEMP-COMP216")
    time.sleep(2)

client_pub.loop_stop()
client_pub.disconnect()