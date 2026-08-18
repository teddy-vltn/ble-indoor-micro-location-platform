from PyObjCTools import AppHelper
import CoreBluetooth

import lib.utils as utils
import lib.models.ibeaconcache as iBeaconCache

beacons = iBeaconCache.iBeaconCache()  # Instantiate the iBeacon cache


class BeaconScanner(object):
    """
    A class that scans for iBeacons using CoreBluetooth framework on Darwin (macOS).
    """

    def centralManagerDidUpdateState_(self, central):
        """
        Callback function that gets called when the state of the central manager changes.
        """
        if central.state() == CoreBluetooth.CBCentralManagerStatePoweredOn:
            print("Darwin: Bluetooth est activé. Recherche des périphériques...")
            central.scanForPeripheralsWithServices_options_(None, None)

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(
        self, central, peripheral, data, rssi
    ):
        """
        Callback function that gets called when a peripheral is discovered.
        """
        raw_data = data.objectForKey_(
            CoreBluetooth.CBAdvertisementDataManufacturerDataKey
        )

        if raw_data is None:
            return

        raw_data = raw_data.hex()

        b = utils.raw_data_to_ibeacon(raw_data, rssi)

        if b is None:
            return

        beacon = beacons.get_beacon(b.get_uuid())
        if beacon is None:
            beacons.add_beacon(b)
            print(f"iBeacon détecté: {b.get_uuid()}")
        else:
            beacon.change_rssi(rssi)


if __name__ == "__main__":
    delegate = BeaconScanner()

    manager = CoreBluetooth.CBCentralManager.alloc()
    manager.initWithDelegate_queue_(delegate, None)

    AppHelper.runConsoleEventLoop()
