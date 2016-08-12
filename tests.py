import boto
from boto.s3.key import Key
from moto import mock_s3


@mock_s3
def test_my_model_save():
    conn = boto.connect_s3()
    bucket = conn.create_bucket('mybucket')

    k = Key(bucket, 'beer')
    k.set_contents_from_string('tasty')

    assert conn.get_bucket('mybucket').get_key('beer').get_contents_as_string() == 'tasty'
