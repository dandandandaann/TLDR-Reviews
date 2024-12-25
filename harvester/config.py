import logging
from configparser import ConfigParser

logger = logging.getLogger(__name__)

def load_config(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            config_string = file.read()
        config_secrets = ConfigParser()
        config_secrets.read_string(config_string)
    except Exception as e:
        logger.error("An error occurred loading the '%s' config file: %s", file_path, e)
        raise

    return config_secrets

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)