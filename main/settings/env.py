import json
import os


env_file_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(env_file_dir, '.env.json'), 'r') as f:
    creds = json.loads(f.read())
    for key, value in creds.items():
        os.environ[key] = value
