import boto
import boto3
from boto.s3.key import Key
from moto import mock_s3


@mock_s3
def test_my_model_save():
    conn = boto.connect_s3()
    bucket = conn.create_bucket('mybucket')

    k = Key(bucket, 'beer')
    k.set_contents_from_string('tasty')

    assert conn.get_bucket('mybucket').get_key('beer').get_contents_as_string() == 'tasty'


@mock_s3
def test_boto3():
    s3 = boto3.resource('s3')
    bucket = s3.create_bucket(Bucket='mybucket')
    s3.Object('mybucket', 'beer').put(Body='tasty3')
    assert s3.Object('mybucket', 'beer').get() == 'tasty3'
    assert bucket.Object('beer').get()['Body'].read() == 'tasty3'
