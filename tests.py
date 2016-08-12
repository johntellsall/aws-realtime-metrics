import boto3
from moto import mock_s3, mock_sns


@mock_s3
def test_boto3():
    s3 = boto3.resource('s3')
    bucket = s3.create_bucket(Bucket='mybucket')
    s3.Object('mybucket', 'beer').put(Body='tasty3')

    assert s3.Object('mybucket', 'beer').get()['Body'].read() == 'tasty3'
    assert bucket.Object('beer').get()['Body'].read() == 'tasty3'

@mock_sns
def test_sns():
    #sns = boto3.resource('sns')
    client = boto3.client()
    response = client.create_topic(Name='upvote')