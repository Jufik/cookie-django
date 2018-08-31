import json
import string
import random

def generate_secret_key(length=50):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join([random.choice(chars) for i in range(length)])

def main():
    with open(".env.sample.json", "r") as sample_env_file:
        data = json.loads(sample_env_file.read())
        data['django_secret_key'] = generate_secret_key()
        data['db_name'] = "{{ cookiecutter.project_slug }}"
    with open('.env.json', 'w') as env_file:
        json.dump(data, env_file, indent=4, sort_keys=True)
    with open(".env.test.json", "r+") as test_env_file:
        data = json.loads(test_env_file.read())
        data['django_secret_key'] = generate_secret_key()
        data['db_name'] = "{{ cookiecutter.project_slug }}"
        test_env_file.seek(0)
        json.dump(data, test_env_file, indent=4, sort_keys=True)

if __name__ == "__main__":
    main()