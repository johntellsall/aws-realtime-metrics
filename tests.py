import boto
from boto.s3.key import Key
from moto import mock_s3
# from mymodule import MyModel

@mock_s3
def test_my_model_save():
    conn = boto.connect_s3()
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    bucket = conn.create_bucket('mybucket')

    k = Key(bucket)
    k.key = 'beer'
    k.set_contents_from_string('tasty')

    assert conn.get_bucket('mybucket').get_key('beer').get_contents_as_string() == 'tasty'

# def test_app(client):
#     assert client.get(url_for('myview')).status_code == 200
