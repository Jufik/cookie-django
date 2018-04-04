import json
import os


def get_credentials():
    domain = os.environ.get('DOMAIN', '')
    file_ = ".env.json"
    if domain:
        file_ = f".env.{domain}.json"
    print(f'LOADING CREDS FROM FILE {file_}')
    env_file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(env_file_dir, file_), 'r') as f:
        creds = json.loads(f.read())
    return creds


env = get_credentials()
