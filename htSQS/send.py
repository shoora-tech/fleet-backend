import boto3
import json
from db import get_all_positions
# Create SQS client
sqs = boto3.client('sqs')

queue_url = 'shoora-test'

# Send message to SQS queue
results = get_all_positions()
for data in results:
# data = {"key": "value"}
    data = json.dumps(data)
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            
        },
        MessageBody=(
            data
        )
    )

    print(response['MessageId'])