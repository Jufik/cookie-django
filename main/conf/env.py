import configparser
import os

config = configparser.RawConfigParser()
env_file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
config.read(os.path.join(env_file_path, '.env'))

for key, value in config['DEFAULT'].items():
	os.environ[key] = value
