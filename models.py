from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.const import CONF_HOST, EVENT_HOMEASSISTANT_STOP

from .coordinator import BambuCoordinator
from .const import DOMAIN, BRAND, LOGGER


class BambuEntity(CoordinatorEntity[BambuCoordinator]):
    _attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, "08:e9:f6:df:e4:94")},
            name="X1C",
            manufacturer=BRAND,
            model="X1C",
            configuration_url=f"http://{self.platform.config_entry.data[CONF_HOST]}"
        )
