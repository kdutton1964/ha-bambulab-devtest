from datetime import timedelta
import logging

DOMAIN = "bambu_lab"
BRAND = "Bambu Lab"
LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(seconds=10)
