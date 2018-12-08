Experiment of boto3 + service accounts
=====================================

To run this, you must be in a GCP VM configured with service account access.

The shell from the GCP console is good enough, that's were I tested this.

You first want to build this, then drop a file to take a GCP service account token and put that in a format that boto3 likes. Read the instructions below, they come with some scripts to take care of all of this.

### First build

```bash
> virtualenv .
> source bin/activate
> pip install -r requirements.txt
```

### Then prepare the environment

Copy this file to $HOME/fetch_credentials.sh and chmod 755

```bash
#!/bin/bash
token=$(curl http://169.254.169.254/computeMetadata/v1/instance/service-accounts/$LOGNAME@gmail.com/token | jq -r '.access_token')
echo "{ \"SessionToken\": \"$token\", \"Version\": 1, \"AccessKeyId\": \"none\", \"SecretAccessKey\": \"none\" }"
```

### Prepare boto3 config

Run this script to setup your config

```bash
#!/bin/bash
mkdir -p ~/.aws/
config_file=~/.aws/config
if [ ! -f $config_file ]; then
  touch $config_file
  echo "[profile gcs]" > $config_file
  echo "credential_process = $HOME/fetch_credentials.sh" >> $config_file
fi
```

### See it work!

```bash
> (boto3-gcp-test) python main.py
```

### How does it work?

botocore comes with different resolvers to pick up credentials. One of them is the `ProcessResolver` which essential does a Popen on whatever executable you specify in your profile. It excepts some JSON back. The only thing different from mainline botocore is the gcs signature version that we use. I added a GCPAuth signer which sets the Authorization header as a bearer token instead of AWS: <...>.
