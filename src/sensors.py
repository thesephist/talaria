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
    pollInterval = 150

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

    def get_roll(self):
        return YTilt.FindTilt(self.serial_number + '.tilt1').get_currentValue()

    def get_pitch(self):
        return YTilt.FindTilt(self.serial_number + '.tilt2').get_currentValue()

    def get_accel(self):
        return YAccelerometer.FindAccelerometer(self.serial_number + '.accelerometer').get_currentValue()

    def get_gyro(self):
        return YGyro.FindGyro(self.serial_number + '.gyro').get_currentValue()

    def is_online(self):
        return self.module.isOnline()

    def startWatching(self):
        self.is_watching = True

        while self.is_watching and self.is_online():

            pitch = self.get_pitch()
            roll = self.get_roll()
            accel = self.get_accel()
            gyro = self.get_gyro()

            for handler in self.handlers:
                handler.handleMeasurements(
                    pitch=pitch,
                    roll=roll,
                    accel=accel,
                    gyro=gyro
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
