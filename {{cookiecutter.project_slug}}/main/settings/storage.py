from main.jsonenv import env

import datetime

DEFAULT_FILE_STORAGE = 'utils.storage.CustomS3Boto3Storage'
# to use ec2 instance role we need to set None to AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
AWS_ACCESS_KEY_ID = env.get('aws_s3_access_key')
AWS_SECRET_ACCESS_KEY = env.get('aws_s3_secret_key')
AWS_STORAGE_BUCKET_NAME = env.get('aws_s3_bucket')
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

# http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=360)  # 1year
expires_header = expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")

AWS_S3_OBJECT_PARAMETERS = {
    'Expires': expires_header,
    'Cache-Control': 'max-age=31556926',  # 1year
}
