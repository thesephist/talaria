import os, sys

from yoctopuce.yocto_api import YRefParam, YAPI
from yoctopuce.yocto_tilt import YTilt
from yoctopuce.yocto_gyro import YGyro
from yoctopuce.yocto_accelerometer import YAccelerometer

def get_sensor_serial(serial_number = None):
    """
    Attempts to connected to a given sensor
    or any sensor if no serial number is given,
    and return the connected sensor's serial number.
    """
    if (serial_number is not None):
        return serial_number
    else:
        sensor = YTilt.FirstTilt()
        if sensor is None:
            sys.exit('No sensors were detected over USB')

        module = sensor.get_module()
        serial_number = module.get_serialNumber()

    return serial_number

def get_tilt1(serial):
    return YTilt.FindTilt(serial + '.tilt1')

def get_tilt2(serial):
    return YTilt.FindTilt(serial + '.tilt2')

def get_accel(serial):
    return YAccelerometer.FindAccelerometer(serial + '.accelerometer')

def get_gyro(serial):
    return YGyro.FindGyro(serial + '.gyro')

def is_online(device):
    return device.isOnline()

# Setup
if YAPI.RegisterHub('usb', YRefParam()) != YAPI.SUCCESS:
    sys.exit('Connection error: connection through USB failed')

serial = get_sensor_serial()
while is_online(get_tilt1(serial)):
    YAPI.Sleep(300, YRefParam())
    print(get_tilt1(serial).get_currentValue())
