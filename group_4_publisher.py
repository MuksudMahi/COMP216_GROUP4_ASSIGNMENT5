import json
import time
import sys
import random
import threading
from datetime import datetime
import paho.mqtt.client as mqtt
import group_4_data_generator as dg


class Publisher:
    def __init__(self, pub_id):
        self.pub_id = pub_id
        self.generator = dg.DataGenerator()
        self.pub_thread = threading.Thread(target=self.publish(), daemon=True)
        self.pub_thread.start()

    temperature: float = 0
    infinite_loop: bool = True

    def generate_data(self):
        self.temperature = self.generator.val

        outlier = random.randint(1, 100)
        if outlier < 5:
            self.temperature += random.randint(30, 40)
        time.sleep(1)
        payload = {
            "publisher_id": f"{self.pub_id}",
            "temperature": f"{self.temperature:.2f}",
            "unit": "celsius",
            "timestamp": f"{datetime.now()}"
        }
        return payload

    def publish(self):
        broker='mqtt.eclipseprojects.io'
        client = mqtt.Client('Temperature_Outside')
        client.on_connect = self._on_connect
        client.on_disconnect = self._on_disconnect
        client.on_message = self._on_message
        client.on_publish = self._on_publish
        client.connect(broker)

        while self.infinite_loop:
            failure = random.randint(1, 100)
            try:
                retry_limit = 5
                retry = 1
                message = self.generate_data()
                while retry <= retry_limit and (self.temperature > 40 or self.temperature < -20):
                    print(f"Abnormal temperature reading, retrying...")
                    message = self.generate_data()
                    retry += 1
                if retry > retry_limit:
                    print(f"[ERROR] Sensor is not working")
                    raise Exception("SensorError")
                if failure == 100:
                    print(f"[ERROR] Failed to publish data")
                else:
                    data_to_publish = json.dumps(message)
                    client.publish(topic='temperature', payload=data_to_publish, qos=0)
                    print(f"{message}")

            except(KeyboardInterrupt, SystemExit, Exception):
                client.disconnect()
                sys.exit()

    # static methods for mqtt
    def _on_connect(self, client, userdata, flags, rc):
        print(f'connected...rc={str(rc)}')

    def _on_disconnect(self, client, userdata, rc):
        print(f'disconnected...rc={str(rc)}')

    def _on_message(self, client, userdata, msg):
        print('message received...')
        print(f'topic: {msg.topic}, qos: {str(msg.qos)}, message: {str(msg.payload)}')

    def _on_publish(self, client, userdata, mid):
        print(f"Message No.{mid}")


publisher1 = Publisher(pub_id=1)
