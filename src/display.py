# Talaria's custom wrapper around Yoctopuce's (admittedly pretty nice) display API, especially for Tal's Environment Visual UI elements

import os
import sys

from yoctopuce.yocto_api import YAPI
from yoctopuce.yocto_display import YDisplay, YDisplayLayer


class Display:

    serial_number = None
    module = None

    width = 0
    height = 0

    def __init__(self, serial_number=None):
        """
        Attempts to connect to a given display
        or any display if no serial number is given
        """
        if serial_number is not None:
            self.module = YDisplay.FindDisplay(
                serial_number + '.display').get_module()
        else:
            display = YDisplay.FirstDisplay()
            if display is None:
                sys.exit('No displays were detected over USB')
            self.module = display.get_module()

        self.serial_number = self.module.get_serialNumber()

        # set variables for display settings
        self.width = display.get_displayWidth()
        self.height = display.get_displayHeight()

        layer = display.get_displayLayer(0)
        layer.clear()

        layer.drawText(self.width/ 2, self.height / 2, YDisplayLayer.ALIGN.CENTER, "Booting Tal...")

    def is_online(self):
        return self.module.isOnline()
