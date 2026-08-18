import yaml
from dotenv import load_dotenv
import os

load_dotenv()

config_absolute_path = os.getenv('CONFIG_ABSOLUTE_PATH')


def load_config():
    with open(config_absolute_path, 'r') as file:
        config = yaml.safe_load(file)
    return config['graph-positioning']