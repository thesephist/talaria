# Handlers for when measurements change by a certain amount

from sensors import Sensor
from utils import flatscale


class Handler:
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

