import json
import os
import lib.settings as settings

# Global variables
config = {}


def init():
    """
    Initializes the configuration and ibeacons dictionary.
    """
    global config, ibeacons
    config.clear()


def get(key):
    """
    Retrieves a value from the configuration dictionary.

    Parameters:
    key (str): The key for which the value is requested.

    Returns:
    The value associated with the key or None if the key doesn't exist.
    """
    return config.get(key)


def set(key, value):
    """
    Sets a key-value pair in the configuration dictionary.

    Parameters:
    key (str): The key to be set.
    value: The value to be associated with the key.
    """
    config[key] = value


def load_config():
    """
    Loads configuration from a JSON file and updates the global config dictionary.
    """
    global config

    try:
        dir_path = settings.get("root_path")
        config_file_path = os.path.join(dir_path, "config.json")

        with open(config_file_path, "r") as file:
            _config = json.load(file)

        config.update(_config)

        print("Configuration loaded")
    except FileNotFoundError:
        print("Config file not found at:", config_file_path)
    except json.JSONDecodeError:
        print("Error decoding JSON from the config file.")
    except Exception as e:
        print("An error occurred while loading the config:", str(e))
