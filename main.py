from boto3.session import Session
from botocore.client import Config
from botocore.session import Session as BotocoreSession
from botocore import UNSIGNED
from botocore.handlers import set_list_objects_encoding_type_url

import boto3
import requests

log_name = os.environ['LOGNAME']
metadata_url = 'http://169.254.169.254/computeMetadata/v1/instance/'
service_account_path = 'service-accounts/%s@gmail.com/token' % log_name
token_url = '%s%s' % (metadata_url, service_account_path)

def fetch_token():
    resp = requests.get(token_url)
    return resp.json()['access_token']

def sign_with_service_account(request, **kwargs):
    token = fetch_token()
    request.headers['Authorization'] = 'Bearer %s' % token

session = Session(region_name='us-central1')

# This is a workaround for a bug in boto3/gcs integration
session.events.unregister('before-parameter-build.s3.ListObjects',
        set_list_objects_encoding_type_url)

session.events.register_last('request-created.s3',
        sign_with_service_account)

# The rest is pretty self explanatory to anyone who
# is familiar with GCS...
s3 = session.resource('s3',
        endpoint_url='https://storage.googleapis.com',
        config=Config(signature_version=UNSIGNED))

bucket = s3.Bucket('dummy-rodrigo-bucket')
for f in bucket.objects.all():
    print(f.key)
