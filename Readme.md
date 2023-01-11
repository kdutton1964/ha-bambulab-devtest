# ha-bambulab-devtest

This is a working repo for a Bambu Lab X1C Integration into Home Assistant.  It is not production ready, and will be moved to a HACS repo once ready for daily use

## Contribution

1) Create a folder with `custom_components` called `bambu_lab`
2) Fork this repo
3) Clone your fork into the `bambu_lab` folder: `git clone <url> .`

## Requirements

You will need to setup MQTT bridging on your existing MQTT broker.
To do this, edit the `mosquitto.conf` file in your broker and add the following:

```connection bambux1c
address 192.168.1.64:1883
topic device/# in
topic device/# out
try_private false
```

If you then open up something like MQTT Explorer and connect to your MQTT Broker, you will see the `device` topic where you can grab the serial number.
A more indepth guide to setup MQTT Bridging for Home Assistant can be found here: https://hackmd.io/@phdunimed/mqttbridging
