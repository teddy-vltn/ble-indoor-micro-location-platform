from bluepy.btle import Scanner, DefaultDelegate
import lib.utils as utils
import lib.models.ibeaconcache as iBeaconCache

beacons = iBeaconCache.iBeaconCache()


class BeaconScanner(DefaultDelegate):
    """
    A class for scanning and detecting iBeacons using Bluetooth Low Energy (BLE) on Linux.

    Methods:
    - __init__(): Initializes the BeaconScanner object and prints a message indicating that Bluetooth
        is enabled and searching for devices.
    - handleDiscovery(dev, isNewDev, isNewData): Overrides the DefaultDelegate's handleDiscovery method to handle the discovery
        of new devices and data. If a new iBeacon is detected,
        it is added to the beacons cache dictionary
        and a message is printed indicating that an iBeacon has been detected.
        If an existing iBeacon is detected, its RSSI is updated and a message is printed indicating that
        the iBeacon has been updated.
    """

    def __init__(self):
        print("Linux: Bluetooth est activé. Recherche des périphériques...")
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev or isNewData:
            for (adtype, desc, value) in dev.getScanData():
                if desc == "Manufacturer":
                    raw_data = value
                    b = utils.raw_data_to_ibeacon(raw_data, dev.rssi)

                    if b is None:
                        return

                    beacon = beacons.get_beacon(b.get_uuid())
                    if beacon is None:
                        beacons.add_beacon(b)
                    else:
                        beacon.change_rssi(dev.rssi)


if __name__ == "__main__":
    scanner = Scanner().withDelegate(BeaconScanner())
    while True:
        try:
            devices = scanner.scan(10.0, passive=True)
        except Exception as e:
            print(f"Une erreur est survenue : {e}")
