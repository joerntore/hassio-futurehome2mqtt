import json
from pyfimptoha.base import Base

class Binary_sensor(Base):
    '''Implementation of MQTT binary_sensor
    https://www.home-assistant.io/integrations/sensor.mqtt

    Device class:
    https://www.home-assistant.io/integrations/sensor/#device-class
        None                Supported
        power               Supported
        presence            Supported
    '''

    _device_class = None
    _expire_after = 0
    _icon = None
    _name_prefix = ""
    _value_template = None

    _init_value = None

    def __init__(self, service_name, service, device):
        '''
        Example
        service_name:   sensor_power
        service (json): {'addr': '/rt:dev/rn:zw/ad:1/sv:sensor_power/ad:41_0' ...
        device (json):  {'client': {'name': 'Ovn (gang)'}, 'fimp': {'adapter': 'zwave-ad', ...
        '''
        super().__init__(service_name, service, device, "binary_sensor")
        self._name = self.name_prefix + self._name

        self._value_template = "{{ value_json.val }}"

        self.set_type()

    @staticmethod
    def supported_services():
        binary_sensors = [
            'sensor_presence',
        ]
        return binary_sensors

    @property
    def icon(self):
        '''Return the icon of the sensor.'''
        return "mdi:" + self._icon


    @property
    def name_prefix(self):
        '''Return the name prefix for this sensor.'''
        return self._name_prefix

    def set_type(self):
        '''
        Set various properties like name prefix and
        device class based on "service_name"
        '''

        device_class = None
        prefix = ""


        
        if self._service_name  == "sensor_presence":
            device_class = "motion"
            prefix = "Motion: "
            

            if 'presence' in self._device['param']:
                self._init_value = self._device['param']['presence']
        

        self._device_class = device_class
        self._name_prefix = prefix


    def get_component(self):
        '''Returns MQTT component to HA'''
        
        payload = {
            "name": self._name,
            "state_topic": self._state_topic,
            "unique_id": self.unique_id,
            "value_template": self._value_template,
            "payload_off": False,
            "payload_on": True,
        }

        if self._device_class:
            payload["device_class"] = self._device_class

        if self._expire_after:
            payload["expire_after"] = self._expire_after

        if self._icon:
            payload["icon"] = self.icon

        device = {
            "topic": self._config_topic,
            "payload": json.dumps(payload),
        }

        return device

    def get_init_state(self):
        '''Return the initial state of the sensor'''
        payload = {"val": self._init_value}
        data = [
            {"topic": self._state_topic, "payload": json.dumps(payload)},
        ]

        return data
