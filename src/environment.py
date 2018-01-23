import sys
import threading # for managing watch / draw loops

from yoctopuce.yocto_api import YAPI, YRefParam

from sensors import Sensor
from display import Display

from apps.reader import ReaderApp
from apps.tracer import TracerApp

from services.network import NetworkService


class Environment(object):
    """
    Represents the virtual environment -- the 'OS'
    behind Tal, which manages all other running apps and services,
    and centrally monitors and dispatches updates to Tals
    peripherals.
    """

    ENABLED_APPS = [
        ReaderApp,
        TracerApp,
    ]
    ENABLED_SERVICES = [
        NetworkService,
    ]
    activeHandlers = []
    activeSession = None
    runningServices = []

    message = ''
    tiltSensorRight = None
    tiltSensorLeft = None  # for now
    display = None

    def __init__(self):
        self.beforeStartUp()
        self.startUp()
        self.afterStartUp()

    def beforeStartUp(self):
        self.message = 'Starting up ...'

    def startUp(self):
        if YAPI.RegisterHub('usb', YRefParam()) != YAPI.SUCCESS:
            sys.exit('Connection error: connection through USB failed')

        # start sensors
        self.tiltSensorRight = Sensor()

        # start display
        self.display = Display()

        # start update loop
        def loop():
            threading.Timer(1, loop).start()

            # update handlers once
            pitch = self.get_pitch()
            roll = self.get_roll()
            accel = self.get_accel()
            gyro = self.get_gyro()
            for h in self.activeHandlers:
                h.handleMeasurements(
                    pitch=pitch,
                    roll=roll,
                    accel=accel,
                    gyro=gyro
                )

            self.display.updateStatus()
            self.display.updateMessage(self.message)
        
        loop()

    def afterStartUp(self):
        self.message = 'Idle'

    def beforeStartApp(self, app):
        if app not in self.ENABLED_APPS:
            return False
        self.message = 'Starting {}...'.format(app.name)

    def startApp(self, app):
        if app in self.ENABLED_APPS:
            self.activeSession = app(environment=self)
        else:
            return False

    def afterStartApp(self, app):
        self.message = 'Running {}'.format(app.name)

    def beforeCloseApp(self, app):
        if not self.activeSession:
            return False
        self.activeSession.beforeClose()

    def closeApp(self, app):
        if not self.activeSession:
            return False
        self.activeSession = None

    def afterCloseApp(self, app):
        return

    def registerHandler(self, handlerInstance):
        self.activeHandlers.append(handlerInstance)

    def unregisterHandler(self, handlerInstance):
        self.activeHandlers.remove(handlerInstance)
