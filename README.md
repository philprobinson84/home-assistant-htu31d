# home-assistant-htu31d

A simple Python app that reads temperature and humidity values from HTU31D I2C sensor and reports to an MQTT broker in a format compatible with Home Assistant.

On initialisation a message is published to the config MQTT topic to add the sensors to Home Assistant using the MQTT Discovery service.

The sensor name added to Home Assistant is the Host Name of the sensor, typically a Raspberry Pi.

## Hardware Setup

This is expected to run on a Raspberry Pi - tested on both the Pi4 and Pi2.

Connect the Adafruit HTU31D sensor to I2C bus 1.

Enable I2C using raspi-config.

## Installation

You'll need an MQTT broker, the code assumes it's on the same machine. In the code, change `localhost` to match the IP of the MQTT broker if this is not the case.

Clone this repo.

Install dependencies:

```bash
sudo apt-get install -y i2c-tools libgpiod-dev
```

Setup virtual env:

```bash
python -m venv venv
```

Activate the venv:

```bash
source venv/bin/activate
```

Install python dependencies:

```bash
pip install -r requirements.txt
```

Exit the venv:

```bash
exit
```

Copy service file:
```bash
sudo cp ./home-assistant-htu31d.service /lib/systemd/system/
```

Reload the system manager:
```bash
sudo systemctl daemon-reload
```

Enable the service:
```bash
sudo systemctl enable home-assistant-htu31d.service
```

Start the service
```bash
sudo systemctl start home-assistant-htu31d.service
```

Check status:
```bash
sudo systemctl status home-assistant-htu31d.service
```

As long as Home Assistant is already integrated wih your MQTT broker, new sensors as entities: `sensor.<HOSTNAME>_temperature_htu31d` and `sensor.<HOSTNAME>_humidity` will be added.
