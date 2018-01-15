# Handlers for when measurements change by a certain amount

from sensors import Sensor

class Handler:

    """
    A Handler represents a listener that responds on every
    measurement event of the sensor.
    """

    description = ''

    def __init__(self, description=''):
        self.description = description

        print('Handler "{}" created'.format(description))

    def listenTo(self, sensor):
        sensor.attachHandler(self)
        print('Handler "{}" started and listening'.format(self.description))

    def stopListening(self, sensor):
        sensor.detachHandler(self)
        print('Handler "{}" stopped listening'.format(self.description))

    def handleMeasurements(self, pitch=None, roll=None, accel=None, gyro=None):
        print(str(pitch) + ' ' + str(roll))
        # do nothing for now, should be overridden in children
