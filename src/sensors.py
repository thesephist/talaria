import os
import sys

from yoctopuce.yocto_api import YAPI
from yoctopuce.yocto_tilt import YTilt
from yoctopuce.yocto_gyro import YGyro
from yoctopuce.yocto_accelerometer import YAccelerometer


class Sensor(object):

    """
    Talaria's custom wrappers around Yoctopuce's
    (admittedly pretty nice) sensors API
    """

    serial_number = None
    module = None
    handlers = []
    is_watching = False
    pollInterval = 50

    rollSensor = None
    pitchSensor = None
    accelSensor = None
    gyroSensor = None

    previousRoll = 0
    previousPitch = 0
    previousAccel = 0
    previousGyro = 0

    def __init__(self, serial_number=None):
        """
        Attempts to connected to a given sensor
        or any sensor if no serial number is given
        """
        if serial_number is not None:
            self.module = YTilt.FindTilt(serial_number + '.tilt1').get_module()
        else:
            # Assume all sensors we're connected to here have a tilt sensor
            sensor = YTilt.FirstTilt()
            if sensor is None:
                print('No sensors were detected over USB. Ignoring...')
                return
            self.module = sensor.get_module()

        self.serial_number = self.module.get_serialNumber()

        # Initialize all onboard sensors
        self.rollSensor = YTilt.FindTilt(self.serial_number + '.tilt1')
        self.pitchSensor = YTilt.FindTilt(self.serial_number + '.tilt2')
        self.accelSensor = YAccelerometer.FindAccelerometer(self.serial_number + '.accelerometer')
        self.gyroSensor = YGyro.FindGyro(self.serial_number + '.gyro')

        # Register advertised value change callbacks
        self.rollSensor.registerValueCallback(self.rollChangedCallback)
        self.pitchSensor.registerValueCallback(self.pitchChangedCallback)
        self.accelSensor.registerValueCallback(self.accelChangedCallback)
        self.gyroSensor.registerValueCallback(self.gyroChangedCallback)

    def get_roll(self):
        return self.rollSensor.get_currentValue()

    def get_pitch(self):
        return self.pitchSensor.get_currentValue()

    def get_accel(self):
        return self.accelSensor.get_currentValue()

    def get_gyro(self):
        return self.gyroSensor.get_currentValue()

    def is_online(self):
        return self.module.isOnline()

    def rollChangedCallback(self, id, value):
        self.previousRoll = float(value)

    def pitchChangedCallback(self, id, value):
        self.previousPitch = float(value)

    def accelChangedCallback(self, id, value):
        self.previousAccel = float(value)

    def gyroChangedCallback(self, id, value):
        self.previousGyro = float(value)

    def startWatching(self):
        self.is_watching = True

        while self.is_watching and self.is_online():
            for handler in self.handlers:
                handler.handleMeasurements(
                    pitch=self.previousPitch,
                    roll=self.previousRoll,
                    accel=self.previousAccel,
                    gyro=self.previousGyro
                )
            YAPI.Sleep(self.pollInterval)

    def stopWatching(self):
        self.is_watching = False

    def attachHandler(self, handler):
        """
        Add a handler and trigger its handler
        every time a new measurement is polled.
        """
        if handler not in self.handlers:
            self.handlers.append(handler)

    def detachHandler(self, handler):
        """
        If a handler was previously listening to
        this sensor, then this takes it off the
        internal list so it stops listening to this
        sensor.
        """
        if handler in self.handlers:
            self.handlers.remove(handler)
