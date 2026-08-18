from lib.models.ibeacon import iBeacon


class iBeaconCache:
    """
    A class to manage a cache of iBeacon devices.

    Attributes:
    cache (dict): A dictionary to store iBeacon devices, keyed by their identifier.

    Methods:
    add_beacon(beacon): Adds or updates an iBeacon in the cache.
    get_beacon(identifier): Retrieves an iBeacon from the cache using its identifier.
    """

    def __init__(self):
        self.cache = {}

    def add_beacon(self, beacon):
        """
        Adds or updates an iBeacon in the cache.

        Args:
        beacon (iBeacon): The iBeacon device to be added or updated.
        """
        if not isinstance(beacon, iBeacon):
            raise TypeError("beacon must be an instance of iBeacon")
        self.cache[beacon.identifier] = beacon

    def get_beacon(self, identifier):
        """
        Retrieves an iBeacon from the cache using its identifier.

        Args:
        identifier (str): The identifier of the iBeacon.

        Returns:
        iBeacon: The iBeacon device if found, else None.
        """
        return self.cache.get(identifier)
