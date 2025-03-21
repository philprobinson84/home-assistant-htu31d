import paho.mqtt.client as mqtt 
import socket
import json
from time import sleep
import board
import adafruit_htu31d

mqttBroker ="10.0.5.100" 
room = socket.gethostname()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, f"{room} Room Temperature")
client.connect(mqttBroker)
client.loop_start()

i2c = board.I2C()  # uses board.SCL and board.SDA
htu = adafruit_htu31d.HTU31D(i2c)

def registerSensors():
    # temp
    config = {"name": f"{room} temperature", "device_class": "temperature", "unit_of_measurement": "°C", "state_topic": f"homeassistant/sensor/{room.lower()}/HTU31D_temperature", "unique_id": f"{room.lower()}_HTU31D_temperature"}
    print(f"Registering sensor: {config}")
    client.publish(f"homeassistant/sensor/{room.lower()}/HTU31D_temperature/config", json.dumps(config))
    # humidity
    config = {"name": f"{room} humidity", "device_class": "humidity", "unit_of_measurement": "%", "state_topic": f"homeassistant/sensor/{room.lower()}/HTU31D_humidity", "unique_id": f"{room.lower()}_HTU31D_humidity"}
    print(f"Registering sensor: {config}")
    client.publish(f"homeassistant/sensor/{room.lower()}/HTU31D_humidity/config", json.dumps(config))

registerSensors()
loopCount = 0
while True:
    loopCount += 1
    if loopCount % 10 == 0:
        registerSensors()
    temperature, humidity = htu.measurements
    print(f"HTU31D: Temperature: {round(temperature, 1)}, Humidity: {round(humidity, 1)}")
    client.publish(f"homeassistant/sensor/{room.lower()}/HTU31D_temperature", round(temperature, 1))
    client.publish(f"homeassistant/sensor/{room.lower()}/HTU31D_humidity", round(humidity, 1))
    sleep(30)
