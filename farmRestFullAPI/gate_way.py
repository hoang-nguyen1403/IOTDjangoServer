import sys

from Adafruit_IO import MQTTClient
import requests

AIO_USERNAME = "tientran1122"
AIO_KEY = "aio_CXqc129ftexBcfrDYyE9vYPt3jO6"
AIO_FEED_IDS = ["bbc-led", "fan", "soil-moisture", "temperature", "light-intensity"]
BASE_URL = 'http://127.0.0.1:8000/api/roomcondition/'


class IotGateWay:
    def __init__(self, user_name, key, feed_ids):
        self.client = MQTTClient(user_name, key)
        self.feed_ids = feed_ids
        self.last_fan_action = "OFF"
        self.last_led_action = "OFF"
        self.last_pump_action = "OFF"
        self.new_temperature_value = None
        self.new_soil_moisture_value = None
        self.new_light_intensity_value = None

    def connect_adafuit(self):
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()

    def connected(self, _):
        print("Connected success...")
        for feed in self.feed_ids:
            self.client.subscribe(feed)

    def subscribe(self, userdata, mid, granted_qos, _):
        print("Subscribe success...")

    def disconnected(self):
        print("Disconnected success...")
        sys.exit(1)

    def message(self, _, feed_id, payload):
        try:
            value = float(payload)
        except ValueError:
            return
        data = {
            "temperature": "0",
            "soilmoisture": "0",
            "light_intensity": "0"
        }
        if feed_id == "temperature":
            self.new_temperature_value = value
            data["temperature"] = value
        if feed_id == "light-intensity":
            self.new_light_intensity_value = value
            data["temperature"] = value
        if feed_id == "soil-moisture":
            self.new_soil_moisture_value = value
            data["soilmoisture"] = value
        r = requests.post(BASE_URL, data=data, auth=("admin", "1"))

    def led_action(self, action: str):
        if action in ['ON', 'OFF']:
            self.client.publish("bbc-led", action)

    def fan_action(self, action: str):
        if action in ['ON', 'OFF']:
            self.client.publish("fan", action)

    def pump_action(self, action: str):
        if action in ['ON', 'OFF']:
            self.client.publish("pump", action)


def go():
    gate_way = IotGateWay(AIO_USERNAME, AIO_KEY, AIO_FEED_IDS)
    gate_way.connect_adafuit()
    print("Connected Adafruit")
    return gate_way


if __name__ == "__main__":
    go()
