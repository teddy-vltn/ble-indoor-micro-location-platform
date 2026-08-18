import platform


def init():
    """
    Initializes the BLE scanner based on the operating system.

    For Linux, imports the linux.blescanner module and starts scanning for beacons.
    For macOS, imports the macos.blescanner module and starts the CoreBluetooth central manager. (used for basic overall testing)
    Raises an exception for unsupported operating systems.
    """
    os_type = platform.system()
    if os_type == "Linux":
        import lib.linux.blescanner as blescanner

        scanner = blescanner.Scanner().withDelegate(blescanner.BeaconScanner())
        while True:
            try:
                scanner.scan(0.2, passive=True)
            except Exception as e:
                print(f"Une erreur est survenue : {e}")

    elif os_type == "Darwin":  # macOS est identifié par 'Darwin'
        import lib.macos.blescanner as blescanner

        # Définir le délégué
        delegate = blescanner.BeaconScanner()

        # Configurer le gestionnaire central
        manager = blescanner.CoreBluetooth.CBCentralManager.alloc()
        manager.initWithDelegate_queue_(delegate, None)

        # Démarrer l'application
        blescanner.AppHelper.runConsoleEventLoop()
    else:
        raise Exception("OS non supporté")
