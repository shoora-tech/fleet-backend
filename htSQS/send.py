import boto3
import json
# Create SQS client
sqs = boto3.client('sqs')

queue_url = 'shoora-test'

# Send message to SQS queue
data = {"key": "value"}
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