import platform
import sys

from datetime import datetime, timedelta

from sensors import Sensor
from utils import flatscale

if platform.system() == 'Darwin': # macOS
    from Quartz.CoreGraphics import (
        CGEventCreateMouseEvent, CGEventPost,
        kCGEventMouseMoved, kCGEventLeftMouseDown,
        kCGEventLeftMouseUp, kCGMouseButtonLeft,
        kCGHIDEventTap,
    )

class Handler(object):
    """
    A Handler represents a listener that responds on every
    measurement event of the sensor.
    """
    description = 'Generic Handler'

    def __init__(self, description=None):
        if description is not None:
            self.description = description
        print('Handler "{}" created'.format(self.description))

    def listenTo(self, sensor):
        sensor.attachHandler(self)
        print('Handler "{}" started and listening'.format(self.description))

    def stopListening(self, sensor):
        sensor.detachHandler(self)
        print('Handler "{}" stopped listening'.format(self.description))

    def handleMeasurements(self, pitch=None, roll=None, accel=None, gyro=None):
        # do nothing for now, should be overridden in children
        return


class PrintOctothorpeHandler(Handler):
    """
    Prints up to '#'s depending on the pitch and roll angles
    """

    description = 'Print octothorpe handler'

    def handleMeasurements(self, pitch=None, roll=None, accel=None, gyro=None):
        length = int(flatscale(pitch, -90, 90) * 25) * 2
        centerOffset = int(flatscale(roll, -90, 135) * 50)
        leftOffset = centerOffset - (length / 2) + 10

        print(' ' * leftOffset + '#' * length)


class LuxControlHandler(Handler):
    """
    Turns a light on and off using a custom "lux" interface from my shell
    """

    description = "Lux lightbulb handler"

    lastTime = datetime.now()
    lastPitch = 0
    luxPowerOn = None

    # degrees per second
    THRESHOLD_PITCH_CHANGE_RATE = 75

    def _turnLightOn(self):
        if self.luxPowerOn is not True:
            from subprocess import Popen
            print('Turning light on!')
            p = Popen(['lux', 'on'])
            self.luxPowerOn = True

    def _turnLightOff(self):
        if self.luxPowerOn is not False:
            from subprocess import Popen
            print('Turning light off!')
            p = Popen(['lux', 'off'])
            self.luxPowerOn = False

    def handleMeasurements(self, pitch=None, roll=None, accel=None, gyro=None):
        currentTime = datetime.now()
        timeSpan = self.lastTime - currentTime # timeSpan (timedelta) is always positive

        # degrees per second
        pitchChangeRate = (pitch - self.lastPitch) / ((timeSpan.microseconds) * 0.000001)

        if pitchChangeRate > self.THRESHOLD_PITCH_CHANGE_RATE:
            self._turnLightOn()
        elif pitchChangeRate < -(self.THRESHOLD_PITCH_CHANGE_RATE):
            self._turnLightOff()

        self.lastTime = currentTime
        self.lastPitch = pitch


class MacOSMouseControlHandler(Handler):
    """
    Controls the mouse cursor on macOS environments
    """

    if platform.system() != 'Darwin':
        print('MacOSMouseControlHandler is not available on the {} platform.'.format(platform.system()))
        sys.exit(1)

    HEIGHT = 1200
    WIDTH = 1920

    def _mouseEvent(self, type, x, y):
        evt = CGEventCreateMouseEvent(
            None,
            type,
            (x, y),
            kCGMouseButtonLeft
        )
        CGEventPost(kCGHIDEventTap, evt)

    def _mouseMove(self, x, y):
        self._mouseEvent(kCGEventMouseMoved, x, y)

    def handleMeasurements(self, pitch=None, roll=None, accel=None, gyro=None):
        # normalized means out of [0, 1]
        normalizedPitch = 1 - flatscale(pitch, -60, 45)
        normalizedRoll = flatscale(roll, -10, 120)

        self._mouseMove(self.WIDTH * normalizedRoll, self.HEIGHT * normalizedPitch)
