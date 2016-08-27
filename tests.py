'''
tests.py -- test AWS Realtime Metrics funcs and APIs

USAGE
py.test tests.py

- fast mode skips calling network AWS APIs:
SKIP_API=1 py.test tests.py
'''

import datetime
import json
import logging
import os

import boto3
import pytest
from moto import mock_s3, mock_sns, mock_sqs


SKIP_API = os.environ.has_key('SKIP_API')
logger = logging.getLogger(__name__)


def format_unique_name(prefix):
    return '{}-{}'.format(
        prefix, datetime.datetime.now().strftime("%H%M%S-%f"))


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


def _test_sqs(queuename):
    sqs = boto3.resource('sqs')
    queue = sqs.create_queue(QueueName=queuename)

    queue.send_message(MessageBody=json.dumps({'beer': 'tasty'}))

    messages = queue.receive_messages()
    assert len(messages) == 1
    assert messages[0].body == '{"beer": "tasty"}'

@mock_sqs
def test_sqs_mock():
    _test_sqs('test')

@pytest.mark.skipif('SKIP_API')
def test_sqs():
    qname = format_unique_name('test-sqs')
    try:
        _test_sqs(qname)
    finally:
        sqs = boto3.resource('sqs')
        sqs.get_queue_by_name(QueueName=qname).delete()
