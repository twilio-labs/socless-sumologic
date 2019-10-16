'''Test event_endpoint'''
# pylint: disable=protected-access
# pylint: disable=wrong-import-position
# pylint: disable=redefined-outer-name
import os, json, boto3, pytest
from requests import exceptions
from moto import mock_dynamodb2

boto3.setup_default_session() # use moto instead of boto

import responses # because moto breaks requests
responses.add_passthru('https://')# moto+requests needs this
responses.add_passthru('http://')# moto+requests needs this

# Method to load test case from external file
EVENT_FILE = os.path.join(
   os.path.dirname(__file__),
   'events',
   'event_endpoint.json'
)

@pytest.fixture()
def event(event_file=EVENT_FILE):
   '''Trigger event'''
   with open(event_file) as f:
      return {"body" : json.dumps(json.load(f))}

@pytest.fixture()
def context():
   class Context(object):
      def __init__(self, timeout, arn_string, version_name):
         self.function_name = "undefined"
         self.function_version = version_name
         self.invoked_function_arn = arn_string
         self.memory_limit_in_mb = 0
         self.aws_request_id = "undefined"
         self.log_group_name = "undefined"
         self.log_stream_name = "undefined"
         self.identity = None
         self.client_context = None
         self.timeout = timeout
         # self.duration = timedelta(seconds=timeout)
   _context = Context(60, "arn:aws:lambda:us-west-2:123456789012:function:foobar", "2.0")
   return _context

import functions.event_endpoint.lambda_function as lambda_function

@mock_dynamodb2
def test_lambda_handler(event, context):
   #setup tables
   boto3.setup_default_session()
   client = boto3.client('dynamodb')
   events_table_name = os.environ['SOCLESS_EVENTS_TABLE']
   events_table = client.create_table(
      TableName=events_table_name,
      KeySchema=[{'AttributeName': 'id','KeyType': 'HASH'}],
      AttributeDefinitions=[])
   
   results_table_name = os.environ['SOCLESS_RESULTS_TABLE']
   results_table = client.create_table(
      TableName=results_table_name,
      KeySchema=[{'AttributeName': 'execution_id','KeyType': 'HASH'}],
      AttributeDefinitions=[])

   #test lambda_handler
   response = lambda_function.lambda_handler(event, context)

   assert response.get("statusCode") == 200