import json

from django.conf import settings

import boto3


class Queue:
    queue_url = settings.RUNS_SQS_QUEUE

    def __init__(self):
        self.client = boto3.client(
            service_name="sqs",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def send_message(self, body):
        self.client.send_message(
            QueueUrl=self.queue_url, MessageBody=body, MessageGroupId="0"
        )

    def post_run(self, run_id, program_name):
        message_body = json.dumps(dict(run_id=run_id, program_name=program_name))
        self.send_message(body=message_body)
