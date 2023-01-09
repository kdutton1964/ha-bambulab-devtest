from homeassistant.helpers.typing import ConfigType

class MqttClientSetup:
    def __init__(self, config: ConfigType) -> None:
        import paho.mqtt.client as mqtt

        self._client = mqtt.Client()
        self._client.enable_logger()

    @property
    def client(self):
        return self._client
