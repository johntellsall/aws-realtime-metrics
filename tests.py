import json

import boto3
from moto import mock_s3, mock_sns, mock_sqs


@mock_s3
def test_boto3():
    s3 = boto3.resource('s3')
    bucket = s3.create_bucket(Bucket='mybucket')

    s3.Object('mybucket', 'beer').put(Body='tasty3')

    assert s3.Object('mybucket', 'beer').get()['Body'].read() == 'tasty3'
    assert bucket.Object('beer').get()['Body'].read() == 'tasty3'


@mock_sns
def test_sns():
    client = boto3.client('sns', 'us-east-1')
    response = client.create_topic(Name='upvote')
    upvote_arn = response['TopicArn']

    response = client.publish(TopicArn=upvote_arn, Message='beer')

    assert len(response['MessageId'])


@mock_sqs
def test_sqs():
    client = boto3.client('sqs', 'us-east-1')
    response = client.create_queue(QueueName='votes')
    queue_url = response['QueueUrl']

    client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps({'beer': 'tasty'}))

    messages = client.receive_messages(QueueUrl=queue_url)
    import ipdb ; ipdb.set_trace()
