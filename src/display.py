import os
import sys
import datetime

from yoctopuce.yocto_api import YAPI, YRefParam
from yoctopuce.yocto_display import YDisplay, YDisplayLayer


class Display(object):

    """
    Represents a generic Yoctopuce display unit,
    containing multiple drawable layers
    """

    serial_number = None
    display = None
    layer_count = 0

    statusLayer = None
    messageLayer = None

    width = 0
    height = 0
    layers = []

    def __init__(self, serial_number=None):
        """
        Attempts to connect to a given display
        or any display if no serial number is given
        """
        if serial_number is not None:
            self.display = YDisplay.FindDisplay(
                serial_number + '.display')
            self.module = self.display.get_module()
        else:
            self.display = YDisplay.FirstDisplay()
            if self.display is None:
                print('No displays were detected over USB. Ignoring...')
                return

        self.module = self.display.get_module()
        self.serial_number = self.module.get_serialNumber()
        
        # set variables for display settings
        self.width = self.display.get_displayWidth()
        self.height = self.display.get_displayHeight()
        self.layer_count = self.display.get_layerCount()
        
        for i in range(0, self.layer_count):
            self.layers.append(self.get_layer(i))

    def is_online(self):
        return self.display.isOnline()

    def get_layer(self, idx=0):
        if idx == 0:
            self.statusLayer = StatusLayer(self.display.get_displayLayer(idx))
            return self.statusLayer
        elif idx == 1:
            self.messageLayer = MessageLayer(self.display.get_displayLayer(idx))
            return self.messageLayer
        else:
            return Layer(self.display.get_displayLayer(idx))

    def clear(self):
        for layer in self.layers:
            layer.clear()

    def updateStatus(self, power=True, busy=False, listening=False, network_connected=False):
        self.statusLayer.power = power
        self.statusLayer.busy = busy 
        self.statusLayer.listening = listening 
        self.statusLayer.network_connected = network_connected

        self.statusLayer.refresh()

    def updateMessage(self, message):
        self.messageLayer.updateMessage(message)

class Layer(object):

    """
    Represents a generic drawable layer in a Yoctopuce
    display unit.

    The first few layers are reserved as special-class, as follows:
    idx     use
    0       environment / operating system status lights
    1       message / text status layer
    2 - 4   application / userland usage
    """

    MARGIN_LEFT = 10
    MARGIN_RIGHT = 4
    MARGIN_TOP = 0
    MARGIN_BOTTOM = 0

    display = None
    display_layer = None

    height = 0
    width = 0

    def __init__(self, display_layer):
        self.display = display_layer.get_display()
        self.display_layer = display_layer

        self.width = display_layer.get_displayWidth()
        self.height = display_layer.get_displayHeight()

        self.clear()
    
    def clear(self):
        self.display_layer.clear()

    def drawText(self, content, vpos='CENTER', hpos='CENTER'):
        position_enum = YDisplayLayer.ALIGN.CENTER
        x = self.width / 2
        y = self.height / 2

        if hpos == 'LEFT':
            x = self.MARGIN_LEFT
            if vpos == 'TOP':
                position_enum = YDisplayLayer.ALIGN.TOP_LEFT
                y = self.MARGIN_TOP
            elif vpos == 'CENTER':
                position_enum = YDisplayLayer.ALIGN.CENTER_LEFT
            elif vpos == 'BOTTOM':
                position_enum = YDisplayLayer.ALIGN.BOTTOM_LEFT
                y = self.height - self.MARGIN_BOTTOM
        elif hpos == 'CENTER':
            if vpos == 'TOP':
                position_enum = YDisplayLayer.ALIGN.TOP_CENTER
                y = self.MARGIN_TOP
            elif vpos == 'CENTER':
                position_enum = YDisplayLayer.ALIGN.CENTER
            elif vpos == 'BOTTOM':
                position_enum = YDisplayLayer.ALIGN.BOTTOM_CENTER
                y = self.height - self.MARGIN_BOTTOM
        elif hpos == 'RIGHT':
            x = self.width - self.MARGIN_RIGHT
            if vpos == 'TOP':
                position_enum = YDisplayLayer.ALIGN.TOP_RIGHT
                y = self.MARGIN_TOP
            elif vpos == 'CENTER':
                position_enum = YDisplayLayer.ALIGN.CENTER_RIGHT
            elif vpos == 'BOTTOM':
                position_enum = YDisplayLayer.ALIGN.BOTTOM_RIGHT
                y = self.height - self.MARGIN_BOTTOM
    
        self.display_layer.drawText(x, y, position_enum, content)

class StatusLayer(Layer):

    """
    The first layer of any display is the status layer,
    used to indicate Talaria system status.

    This is updated at regular time intervals and completely
    independently of all other processes, on a separate
    display layer.
    """

    power = True
    busy = False
    listening = False
    network_connected = False

    def __init__(self, display_layer):
        super(StatusLayer, self).__init__(display_layer)
        self.refresh()

    def _draw_dot(self, status, order):
        if (status):
            self.display_layer.drawDisc(3, order * 8 + 3, 3)
        else:
            self.display_layer.drawCircle(3, order * 8 + 3, 3)

    def refresh(self):
        self.clear()

        self._draw_dot(self.power, 0)
        self._draw_dot(self.busy, 1)
        self._draw_dot(self.listening, 2)
        self._draw_dot(self.network_connected, 3)

class MessageLayer(Layer):

    """
    The second layer of any display is the message layer,
    used to deliver console / debugging and any other
    useful messages to the user alongside application display.

    This is updated independently of other processes, on a
    separate display layer.
    """

    message = 'Idle'

    def __init__(self, display_layer):
        super(MessageLayer, self).__init__(display_layer)
        self.updateMessage(self.message)

    def updateMessage(self, message):
        self.clear()
        self.message = message
        dateStr = datetime.datetime.now().isoformat()
        self.drawText(dateStr[0:10], 'TOP', 'RIGHT')
        self.drawText(dateStr[11:16], 'CENTER', 'RIGHT')
        self.drawText(self.message, 'BOTTOM', 'RIGHT')
