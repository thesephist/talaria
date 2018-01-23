import sys

from sensors import Sensor
from display import Display
from handlers import PrintOctothorpeHandler
# from handlers import LuxControlHandler

from yoctopuce.yocto_api import YRefParam, YAPI

# Setup
if YAPI.RegisterHub('usb', YRefParam()) != YAPI.SUCCESS:
    sys.exit('Connection error: connection through USB failed')

"""

# Application logic 
sensor = Sensor()  # find the first (and only, for now) sensor available in the system
handler = PrintOctothorpeHandler()
# handler = LuxControlHandler()
handler.listenTo(sensor)

# Call last, as this blocks
sensor.startWatching()

"""

# Display Logic
display = Display() # find the first (and only, for now) display available in the system

YAPI.Sleep(10, YRefParam())
