import paho.mqtt.client as mqtt
import time
import json
import threading
from datetime import datetime, timedelta
from tkinter import *
import random


# --- constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DISTANCE = 10
NUMBER = (SCREEN_WIDTH // DISTANCE) + 1


class Subscriber:
    def __init__(self):
        self.client = mqtt.Client("Smartphone")
        sub_thread = threading.Thread(target=self.subscribe(), daemon=True)
        sub_thread.start()

    data = list()
    timestamp = list()
    min_data = 20

    def decode_message(self, message):
        message = message.decode("utf-8")
        payload = json.loads(message)
        # print(payload)
        if len(self.data) < self.min_data:
            self.process_data(payload)
        elif not self.is_corrupt_data(float(payload.get('temperature'))):
            self.process_data(payload)
        else:
            print("ERROR: ignoring corrupt data.")

    def process_data(self, payload):
        self.data.append(float(payload.get('temperature'))+100)
        self.timestamp.append(datetime.strptime(payload.get('timestamp'), "%Y-%m-%d %H:%M:%S.%f"))
        self.gui()


    def is_corrupt_data(self, data):
        values_size = len(self.data)
        samples = self.data[values_size - self.min_data:]
        sorted_samples = sorted(samples)
        P75 = sorted_samples[round(0.75 * len(sorted_samples))]
        P25 = sorted_samples[round(0.25 * len(sorted_samples))]
        IQR = P75 - P25
        LOF = P25 - 3 * IQR
        HOF = P75 + 3 * IQR
        return data < LOF or data > HOF

    def subscribe(self):
        # root.mainloop()
        broker = 'mqtt.eclipseprojects.io'
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.client.on_subscribe = self._on_subscribe
        self.client.on_unsubscribe = self._on_unsubscribe
        self.client.connect(broker)
        self.client.loop_start()
        root.mainloop()


    def gui(self):

        # remove first
        if len(self.data) > NUMBER:
            self.data.pop(0)

        # remove all lines
        canvas.delete('all')
        graph_canvas.delete('all')
        canvas.create_text(100, 20, fill="darkblue", font="Times 20 italic bold",
                           text="Line Chart")
        graph_canvas.create_text(100, 20, fill="darkblue", font="Times 20 italic bold",
                                 text="Bar Chart")
        # draw new lines
        for x, (y1, y2) in enumerate(zip(self.data, self.data[1:])):
            #print(x)
            x1 = x * DISTANCE
            x2 = (x + 1) * DISTANCE
            # Line chart
            canvas.create_line([x1, y1, x2, y2], width=5, fill='green')
            color = ["red", "green", "blue", "pink", "yellow", "violet"]
            # Bar chart
            graph_canvas.create_rectangle(x1, y1, x2, SCREEN_HEIGHT / 2, fill=random.choice(color))

            # run again after 0.5 sec
            # root.after(1000, self.gui)

    # static methods for mqtt
    def _on_connect(self, client, userdata, flags, rc):
        print('connected...rc=' + str(rc))
        client.subscribe(topic='temperature', qos=0)

    def _on_disconnect(self, client, userdata, rc):
        pass
        print('disconnected...rc=' + str(rc))

    def _on_message(self, client, userdata, msg):
        print("Received message --------")
        print('topic: ' + msg.topic + ', qos: ' +
              str(msg.qos) + ', message: ' + str(msg.payload))
        self.decode_message(msg.payload)
        # self.gui()

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        pass
        print('subscribed (qos=' + str(granted_qos) + ')')

    def _on_unsubscribe(self, client, userdata, mid, granted_qos):
        pass
        print('unsubscribed (qos=' + str(granted_qos) + ')')


root = Tk()
root.geometry('{}x{}'.format(SCREEN_WIDTH, SCREEN_HEIGHT + 100))
root.title("Dynamic Display")

canvas = Canvas(root, width=SCREEN_WIDTH / 2, height=SCREEN_HEIGHT / 2, bg="#ffcccc")
canvas.pack(fill='both', expand=True)
graph_canvas = Canvas(root, width=SCREEN_WIDTH / 2, height=SCREEN_HEIGHT / 2, bg='white')
graph_canvas.pack(fill='both', expand=True)
# root.mainloop()

sub = Subscriber()
