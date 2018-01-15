from sensors import Sensor
from handlers import Handler

from yoctopuce.yocto_api import YRefParam, YAPI

# Setup
if YAPI.RegisterHub('usb', YRefParam()) != YAPI.SUCCESS:
    sys.exit('Connection error: connection through USB failed')

# Application logic 
sensor = Sensor()  # find the first (and only, for now) sensor available in the system
handler = Handler('First handler')
handler.listenTo(sensor)

# Call last, as this blocks
sensor.startWatching()
