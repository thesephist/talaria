class App(object):
    """
    Base class for a Tal userland app
    consuming Tal environment APIs.
    """

    name = 'App'

    def __init__(self, environment):
        self.environment = environment

    def afterStart():
        return

    def beforeClose():
        return
