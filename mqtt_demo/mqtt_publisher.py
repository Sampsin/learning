import random
import time
from paho.mqtt import client as mqtt_client

class Mqtt_Publisher:
    def __init__(self, broker_ip='192.168.200.128', client_prefix="pub_", port=1883, timeout=60):
        self.broker_ip = broker_ip #server ip
        self.port = port #network port
        self.timeout = timeout #connect timeout time
        self.connected = False
        self.client_id = client_prefix + str(random.randint(10000,99999)) #create an random integer as client id
        self.start()

    def start(self):
        self.client = mqtt_client.Client(self.client_id)
        self.client.on_connect = self.on_connect
        self.client.connect(self.broker_ip, self.port, self.timeout)
        self.client.loop_start() #default loop to try connection forever until you call disconnect()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
        else:
            raise Exception("Failed to connect mqtt server")
        
    def publish(self, topic, payload, qos=0):
        if self.connected:
            return self.client.publish(topic, payload=payload, qos=qos)
        else:
            raise Exception("mqtt server not connected, cannot publish topic")
        
if __name__=='__main__':
    pub=Mqtt_Publisher()
    while not pub.connected: #waiting for client connection
        time.sleep(0.05)
    print("publisher connect successfully")
    while True:
        pub.publish('topic_test','this is a test message')
        pub.publish('topic_test1/a','this is level2 testa ')
        pub.publish('topic_test1/b','this is level2 testb ')
        pub.publish('topic_test1/a/c','this is level3 testc ')
        time.sleep(1)
