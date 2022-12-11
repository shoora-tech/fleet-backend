from django.core.management.base import BaseCommand, CommandError
# from polls.models import Question as Poll
from alert.models import RealTimeDatabase
import boto3
from environ import Env
from django.conf import settings
import json

# sqs = boto3.client('sqs')
sqs = boto3.client('sqs',
        region_name="ap-south-1",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)


class Command(BaseCommand):
    help = 'Pulls SQS data and push it to RealtimeDatabase'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def change_case(self, str):
        return ''.join(['_'+i.lower() if i.isupper()
                else i for i in str]).lstrip('_')
    
    def format_sqs_data(self, data):
        x = {}
        for key, value in data.items():
            x[self.change_case(key)] = value
        
        return x

    def handle(self, *args, **options):
        response = sqs.receive_message(
            QueueUrl="https://sqs.ap-south-1.amazonaws.com/547686973061/video-telematics",
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            WaitTimeSeconds=20
        )

        messages = response['Messages']
        for msg in messages:
            print("\n------------------------\n")
            # print(type(json.loads(msg['Body'])),msg['Body'])
            print(self.format_sqs_data(json.loads(msg['Body'])))
        # self.stdout.write(self.style.SUCCESS('Successfully polled "%s"' % response))
        # for poll_id in options['poll_ids']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

            