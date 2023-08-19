import sys
import time

from Adafruit_IO import MQTTClient

AIO_USERNAME = "tientran1122"
AIO_KEY = "aio_wPCV55eRclRATSW0dUmcAuJZYcBV"
AIO_FEED_IDS = ["bbc-led", "fan", "soil-moisture", "temperature"]


class IotGateWay:
    def __init__(self, user_name, key, feed_ids):
        self.client = MQTTClient(user_name, key)
        self.feed_ids = feed_ids
        self.last_fan_action = "OFF"
        self.last_led_action = "OFF"
        self.last_pump_action = "OFF"

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
            if payload == "ON":
                value = 1
            else:
                value = 0
        if feed_id == "temperature":
            if value > 30:
                if self.last_fan_action != "ON":
                    self.fan_action("ON")
                    self.last_fan_action = "ON"
            else:
                if self.last_fan_action != "OFF":
                    self.fan_action("OFF")
                    self.last_fan_action = "OFF"
        if feed_id == "light-intensity":
            if value < 20:
                if self.last_led_action != "ON":
                    self.led_action("ON")
                    self.last_led_action = "ON"
            else:
                if self.last_led_action != "OFF":
                    self.led_action("OFF")
                    self.last_led_action = "OFF"
        # if feed_id == "soil-moisture":
        #     if value < 50:
        #         if self.last_pump_action != "ON":
        #             self.pump_action("ON")
        #             self.last_pump_action = "ON"
        #     else:
        #         if self.last_pump_action != "OFF":
        #             self.pump_action("OFF")
        #             self.last_pump_action = "OFF"

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
    # while True:
    #     time.sleep(1)
    # # data = {
    #     "author": 1,
    #     "hasFan": True,
    #     "hasPump": False,
    #     "hasLed": False
    # }
    # my_view(data)
