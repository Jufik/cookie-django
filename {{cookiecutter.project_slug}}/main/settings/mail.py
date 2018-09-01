from main.jsonenv import env

EMAIL_HOST = env.get('email_host')
EMAIL_HOST_USER = env.get('email_host_user')
EMAIL_HOST_PASSWORD = env.get('email_host_password')
EMAIL_PORT = env.get('email_port', 587)
EMAIL_SUBJECT_PREFIX = ""
EMAIL_USE_TLS = env.get('email_use_tls', True)
EMAIL_USE_SSL = env.get('email_use_ssl', False)
DEFAULT_FROM_EMAIL = env.get('default_from_email')