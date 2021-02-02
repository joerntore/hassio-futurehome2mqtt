# Hass.io Add-on: Futurehome FIMP to MQTT

## About

This [Futurehome FIMP](https://github.com/futurehomeno/fimp-api) to MQTT add-on allows you to integrate the Futurehome
Smarthub with Home Assistant by using the local MQTT broker inside the hub.

While it is possible to configure Home Assistant the FIMP protocol
directly is a lot of work, and auto discovery is not possible.

This addon work as a bridge between the [FIMP protocol](https://github.com/futurehomeno/fimp-api)
and the MQTT message system prefered by Home Assistant. In most cases the representation
of the components talk directly via MQTT. However, due to limitations in the Light
component of HA these devices are bridged though separate MQTT topics handled by this addon. At
least I'm unable to do it without.

The author of this addon recognize that this integration should be solved by a
custom platform component for Home Assistant, but the bridge approach was used
to get something working.

There are multiple caveats with the current approach so dedicated component should
be developed as we learn more about the FIMP protocol.

## Supported Futurehome devices

* Appliances (switches in HA)
  * Wall plugs like Fibaro Wall plug is supported
* Lights (lights in HA)
  * Dimmers - On/off and brightness. Tested with Fibaro dimmer 2
  * Wall plugs like Fibaro Wall plug is *not* supported (yet)
* Sensors (sensors in HA)
  * Battery
  * Illuminance
  * Power usage
  * Temperature
* Scene control. Exposed as sensor. Tested with Fibaro button, and Namron 4 channel (K8)
* Modus: home, away, sleep and vacation (`sensor.modus`, read only)

Everything execpt dimmers work without the need of the brigde functionality provided by this addon once they are auto discovered.
These devices can talk to HA directly over MQTT while dimmers needs to be bridged via custom topics for now.

# Configuration and installation

### 1. Home Assistant configuration

Home Assistant must use the MQTT broker on the Futurehome Smart hub.

configuration.yaml
```
# MQTT
mqtt:
  # Futurehome smart hub
  broker: *hub ip*
  username: *username*
  password: *password*
  port: 1884
  discovery: true
  discovery_prefix: homeassistant

# Uptime sensor to detect if Home Assistant is restarted
sensor:
  - platform: uptime
    name: "HA uptime moment"
  - platform: template
    sensors:
      ha_uptime_minutes:
        friendly_name: "HA uptime minutes"
        value_template: >
          {{ ((as_timestamp(now()) - as_timestamp(states('sensor.ha_uptime_moment'))) / 60) | round(0) }}
```

### 2. Install add-on

1) Add this repo as a Hass.io repository
2) Install the addon 'Futurehome FIMP to MQTT'
3) Configure the addon with the same parameters as before
4) Start it. Supported devices should appear in the Home Assistant UI


# Development

As this addon is not dependent on Home Assistant it's easiest to develop
new features locally. Either using virtualenv (se section below) or using
docker.

See https://developers.home-assistant.io/docs/en/hassio_addon_testing.html.

## Using virtual env

### Git clone and installation
```
git clone https://github.com/runelangseid/hassio-futurehome2mqtt
cd hassio-futurehome2mqtt/futurehome2mqtt
virtualenv venv  # You might need to specify python 3 somehow: virtualenv -p python3.7 venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Configuration

1. Create an Long-lived Access token. Needed to detect HA restart

2. Setup configuration
    ```
    cp env-div .env
    ```
3. Edit `.env` and fill in hostnames and credentials

4. Run `source .env`

5. Run `python run.py serve`


# Alternative FIMP integrations

Below are examples on how to add Wall plugs and sensors manually to Home Assistant
using MQTT without the use of this addon.

## Wall plug (Fibaro)

Replace '34' with the address for the device in Futurehome.

```
switch:
  #
  # Kontor
  #
  # Wall plug
  - platform: mqtt
    name: "Wall plug (kontor)"
    state_topic:   "pt:j1/mt:evt/rt:dev/rn:zw/ad:1/sv:out_bin_switch/ad:34_0"
    command_topic: "pt:j1/mt:cmd/rt:dev/rn:zw/ad:1/sv:out_bin_switch/ad:34_0"
    value_template: '{{ value_json.val }}'
    payload_on:  '{"props":{},"serv":"out_bin_switch","tags":[],"type":"cmd.binary.set","val":true,"val_t":"bool"}'
    payload_off: '{"props":{},"serv":"out_bin_switch","tags":[],"type":"cmd.binary.set","val":false,"val_t":"bool"}'
    state_on: true
    state_off: false
```

## Multi Sensor (Fibaro)

Replace '37' with the address for the device in Futurehome.

```
  # Øye (kontor)
  - platform: mqtt
    name: "Batteri Kontor"
    state_topic: "pt:j1/mt:evt/rt:dev/rn:zw/ad:1/sv:battery/ad:37_0"
    unit_of_measurement: '%'
    value_template: "{{ value_json.val }}"
  - platform: mqtt
    name: "Bevegelse Kontor"
    state_topic: "pt:j1/mt:evt/rt:dev/rn:zw/ad:1/sv:sensor_presence/ad:37_0"
    value_template: "{{ value_json.val }}"
  - platform: mqtt
    name: "Temperatur Kontor"
    state_topic: "pt:j1/mt:evt/rt:dev/rn:zw/ad:1/sv:sensor_temp/ad:37_0"
    unit_of_measurement: '°C'
    value_template: "{{ value_json.val }}"
  - platform: mqtt
    name: "Lysstyrke Kontor"
    state_topic: "pt:j1/mt:evt/rt:dev/rn:zw/ad:1/sv:sensor_lumin/ad:37_0"
    unit_of_measurement: 'Lux'
    value_template: "{{ value_json.val }}"
```
