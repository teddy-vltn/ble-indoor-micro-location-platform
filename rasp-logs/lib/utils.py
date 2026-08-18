import lib.models.ibeacon as ibeacon
import lib.settings as settings

MAJOR_FILTER_SIGNAL = settings.get("major_filter_signal")


def raw_data_to_ibeacon(hex_data, rssi):
    """
    Converts raw hexadecimal data to an iBeacon object.

    Parameters:
    hex_data (str): The raw hexadecimal data string.
    rssi (int): The RSSI value associated with the iBeacon.

    Returns:
    iBeacon object or None: The iBeacon object if conversion is successful, else None.
    """

    try:
        # Validate the length of hex_data before processing
        if len(hex_data) < 50:
            return None

        # Extracting identifier and UUID
        identifier = hex_data[:8]
        uuid = hex_data[8:40]

        # Converting major and minor values from hex to int
        major = int(hex_data[40:44], 16)
        minor = int(hex_data[44:48], 16)

        # Check against the major filter signal setting
        if major != MAJOR_FILTER_SIGNAL:
            return None

        # Convert the TX power from hex to signed decimal
        tx_power_hex = hex_data[48:50]
        tx_power = int(tx_power_hex, 16)
        if tx_power_hex[0] > "7":  # Adjust for signed values
            tx_power -= 256

        # Create and return the iBeacon object
        beacon = ibeacon.iBeacon(identifier, uuid, major, minor, tx_power)
        beacon.change_rssi(rssi)
        return beacon

    except Exception as e:
        return None
