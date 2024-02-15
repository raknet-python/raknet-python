class RakPeer:
    def start(self, host: str = None, port: int = 0, max_connections: int = 1):
        """
        Starts the network threads, opens the listen port. This function must be called before connect().
        Multiple calls while the function is already active are ignored. To call this function again with
        different settings, you must first call shutdown().

        Args:
            host (str, optional): The hostname or IP address to listen for connections on. Default is None.
            port (int, optional): The port to listen for connections on. Default is 0.
            max_connections (int, optional): The maximum number of connections between this instance and another
                                             instance. A pure client would set this to 1. A pure server would
                                             set it to the number of allowed clients. A hybrid would set it to the
                                             sum of both types of connections. Default is 1.

        Returns:
            RAKNET_STARTED on success, otherwise appropriate failure enumeration.
        """
        ...
