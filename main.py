from boto3.session import Session
from botocore.client import Config
from botocore.session import Session as BotocoreSession
from botocore.handlers import set_list_objects_encoding_type_url

import boto3

# Create a botocore session using the gcs profile.
# This will go and look for the gcs profile in ~/.aws/config
# This is where we define the credential_process
botocore_session = BotocoreSession(profile='gcs')
session = Session(region_name='us-central1', botocore_session=botocore_session)

# This is a workaround for a bug in boto3/gcs integration
session.events.unregister('before-parameter-build.s3.ListObjects',
        set_list_objects_encoding_type_url)

# The rest is pretty self explanatory to anyone who
# is familiar with GCS...
s3 = session.resource('s3',
        endpoint_url='https://storage.googleapis.com',
        config=Config(signature_version='gcs'))

bucket = s3.Bucket('dummy-rodrigo-bucket')
for f in bucket.objects.all():
    print(f.key)
