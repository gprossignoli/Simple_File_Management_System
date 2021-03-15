import logging
import os
import configparser
from logging.handlers import RotatingFileHandler

ROOT_DIR = os.path.dirname(os.path.abspath("settings.py"))
settings_file = open(os.path.join(ROOT_DIR, "settings.ini"), "r")
config = configparser.ConfigParser()
config.read(os.path.join(ROOT_DIR, "settings.ini"))

SECRET_KEY = config.get('SECRETS', 'flask_key')
DB_NAME = config.get('DB', 'sqlite')
FILES_DIR = config.get('SECRETS', 'files_dir')
CSRF = True

# Flask user config
USER_APP_NAME = "Simple File Management System"  # Shown in and email templates and page footers
USER_ENABLE_EMAIL = False
USER_ENABLE_USERNAME = True
USER_CORPORATION_NAME = "Gerardo"

# LOGGING CONFIG

logger = logging.getLogger('smfs')
logging.basicConfig(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

#to log debug messages
debug_logger = logging.StreamHandler()
debug_logger.setLevel(logging.DEBUG)
debug_logger.setFormatter(formatter)

#to log general messages
# x2 files of 2mb
info_logger = RotatingFileHandler(filename='smfs.log', maxBytes=2097152, backupCount=2)
info_logger.setLevel(logging.INFO)
info_logger.setFormatter(formatter)

#to log errors messages
error_logger = RotatingFileHandler(filename='smfs_errors.log', maxBytes=2097152, backupCount=2)
error_logger.setLevel(logging.ERROR)
error_logger.setFormatter(formatter)

logger.addHandler(debug_logger)
logger.addHandler(info_logger)
logger.addHandler(error_logger)

