import random
import time
from paho.mqtt import client as mqtt_client

class Mqtt_Subscriber:
    def __init__(self, broker_ip='192.168.200.128', client_prefix="sub_", port=1883, timeout=60, topic_name="topic_test"):
        self.broker_ip = broker_ip #server ip
        self.port = port #network port
        self.timeout = timeout #connect timeout time
        self.topic_name = topic_name
        self.connected = False
        self.client_id = client_prefix + str(random.randint(10000,99999)) #create an random integer as client id
        self.start()

    def start(self):
        self.client = mqtt_client.Client(self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_ip, self.port, self.timeout)
        self.client.subscribe(self.topic_name)
        self.client.loop_start() #default loop to try connection forever until you call disconnect()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
        else:
            raise Exception("Failed to connect mqtt server")
        
    def on_message(self, client, userdata, msg): #after subscribing topic, will get topic message, this is the callback function
        print(msg.payload.decode('utf-8')) #simply print message
        
    def subscribe(self, topic, qos=0):
        if self.connected:
            return self.client.subscribe(topic, qos=qos, options=None, properties=None)
        else:
            raise Exception("mqtt server not connected, cannot publish topic")
        
if __name__=='__main__':
    sub=Mqtt_Subscriber(topic_name="topic_test1/#")
    while not sub.connected: #waiting for client connection
        time.sleep(0.05)
    print("subsciber connect successfully")
    sub.subscribe(topic="topic_test")
    while True:
        time.sleep(1)

    