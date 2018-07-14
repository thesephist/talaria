from services.service import Service

class NetworkService(Service):
    """
    Polls for and fetches / sends data asynchronously
    and efficiently to and from Tal.
    """

    connected = False

    def __init__(self):
        super(NetworkService, self).__init__()

    def is_connected(self):
        return self.connected
