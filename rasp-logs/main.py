import signal

import lib.settings as settings
import lib.scanner as scanner

import os

# Récupération de l'identité du scanner, hostname par défaut
hostname = os.uname()[1]

settings.init()
settings.set("root_path", os.path.dirname(os.path.abspath(__file__)))
settings.set("logs_dir_path", os.path.join(settings.get("root_path"), "logs"))
settings.set("hostname", hostname)
settings.load_config()

import lib.logger as logger

# Enregistrement du gestionnaire de signal pour SIGTERM, SIGINT, et SIGHUP
signal.signal(signal.SIGTERM, logger.signal_handler)
signal.signal(signal.SIGINT, logger.signal_handler)
signal.signal(signal.SIGHUP, logger.signal_handler)

logger.init()
logger.log("Démarrage du script")

scanner.init()
