'''Test send_log_message'''
# pylint: disable=protected-access
# pylint: disable=wrong-import-position
# pylint: disable=redefined-outer-name
import os, json, boto3, pytest
from requests import exceptions
from moto import mock_ssm

# boto3.setup_default_session() # use moto instead of boto

import responses # because moto breaks requests
responses.add_passthru('https://')# moto+requests needs this
responses.add_passthru('http://')# moto+requests needs this

# begin testing lambda function
import functions.send_log_message.lambda_function as lambda_function

@pytest.fixture()
def message():
   return "TEST"

@pytest.fixture()
def sumo_ssm_name():
   return "/socless/integration_name/message_url"

@mock_ssm
def test_handle_state(sumo_ssm_name, message):
   #setup param for lambda function
   boto3.setup_default_session()
   client = boto3.client('ssm')
   client.put_parameter(Name=sumo_ssm_name, Type='SecureString', Value='http://twilio.com', KeyId='alias/aws/ssm')

   # run lambda function
   response = lambda_function.handle_state(sumo_ssm_name, message)

   # test response
   assert response.get("status") == "success"

@mock_ssm
def test_handle_state_invalid_message(sumo_ssm_name):
   #setup param for lambda function
   boto3.setup_default_session()
   client = boto3.client('ssm')
   client.put_parameter(Name=sumo_ssm_name, Type='SecureString', Value='http://twilio.com', KeyId='alias/aws/ssm')

   # run lambda function
   with pytest.raises(TypeError):
      response = lambda_function.handle_state(sumo_ssm_name, ['not', 'a', 'string'])

@mock_ssm
def test_handle_state_failed_post(sumo_ssm_name, message):
   #setup failed POST param for lambda function
   client = boto3.client('ssm')
   client.put_parameter(Name=sumo_ssm_name, Type='SecureString', Value='https://httpstat.us/403', KeyId='alias/aws/ssm')

   # run lambda function
   with pytest.raises(exceptions.ConnectionError):
      response = lambda_function.handle_state(sumo_ssm_name, message)


# Method to load test case from external file
# EVENT_FILE = os.path.join(
#    os.path.dirname(__file__),
#    '..',
#    '..',
#    'events',
#    'send_log_message.json'
# )

# @pytest.fixture()
# def event(event_file=EVENT_FILE):
#    '''Trigger event'''
#    with open(event_file) as f:
#       return json.load(f)

