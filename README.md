Experiment of boto3 + service accounts
=====================================

To run this, you must be in a GCP VM configured with service account access.

The shell from the GCP console is good enough, that's were I tested this.

### First build

```bash
> virtualenv .
> source bin/activate
> pip install -r requirements.txt
```

### See it work!

```bash
> (boto3-gcp-test) python main.py
```

### How does it work?
botocore has hooks on the requests lifecycle. One can override how a request is signed. In our example, we pull a token from the GCP metadata service and pass that to the Authorization headers.
