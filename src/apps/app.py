class App(object):
    """
    Base class for a Tal userland app
    consuming Tal environment APIs.
    """

    name = None

    def __init__(self, name='App'):
        self.name = name

    def afterStart():
        return

    def beforeClose():
        return
