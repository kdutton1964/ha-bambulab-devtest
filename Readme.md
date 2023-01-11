# ha-bambulab-devtest

This is a working repo for a Bambu Lab X1C Integration into Home Assistant.  It is not production ready, and will be moved to a HACS repo once ready for daily use

## Contribution

1) Create a folder with `custom_components` called `bambu_lab`
2) Fork this repo
3) Clone your fork into the `bambu_lab` folder: `git clone <url> .`
4) Edit [this line](https://github.com/greghesp/ha-bambulab-devtest/blob/main/sensor.py#L80) with your device serial number from MQTT

## Updates

* Initial configuration flow is functionally working.  `pybambu` is local to this project for now, but this needs to expose the device serial number, so that it can be passed to the unique ID of the Home Assistant Entity
* Only creating a WiFi Signal sensor at the moment until the data can be passed to HA
* Coordinator does not currently get data or return to HA
