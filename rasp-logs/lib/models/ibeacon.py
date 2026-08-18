import lib.logger as logger


class iBeacon:
    """
    A class representing an iBeacon device.

    Attributes:
    identifier (str): The identifier of the iBeacon device.
    uuid (str): The UUID of the iBeacon device.
    major (int): The major value of the iBeacon device.
    minor (int): The minor value of the iBeacon device.
    tx_power (int): The transmit power of the iBeacon device.
    rssi (int): The received signal strength indicator (RSSI) of the iBeacon device.

    Methods:
    read(): Reads the current values of the iBeacon device and logs them.
    change_rssi(rssi): Changes the RSSI value of the iBeacon device and sets the hasChanged flag to True.
    get_uuid(): Returns the UUID of the iBeacon device.
    """

    def __init__(self, identifier, uuid, major, minor, tx_power):
        self.identifier = identifier
        self.uuid = uuid
        self.major = major
        self.minor = minor
        self.tx_power = tx_power
        self.rssi = 0

    def read(self):
        """
        Reads the current values of the iBeacon device and logs them.
        """
        logger.logcsv(
            {
                "major": self.major,
                "minor": self.minor,
                "tx_power": self.tx_power,
                "rssi": self.rssi,
            }
        )

    def change_rssi(self, rssi):
        """
        Changes the RSSI value of the iBeacon device and sets the hasChanged flag to True.

        Args:
        rssi (int): The new RSSI value.
        """
        self.rssi = rssi

        self.read()

    def get_uuid(self):
        """
        Returns the UUID of the iBeacon device.

        Returns:
        str: The UUID of the iBeacon device.
        """
        return self.uuid
