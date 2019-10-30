'''Test send_log_message'''
# pylint: disable=protected-access
# pylint: disable=wrong-import-position
# pylint: disable=redefined-outer-name
from tests.conftest import * #imports testing boilerplate
from requests import exceptions
from moto import mock_ssm

# begin testing lambda function
import functions.send_log_message.lambda_function as lambda_function


MESSAGE = "TEST"

SUMO_SSM_NAME = "/socless/integration_name/message_url"

@mock_ssm
def test_handle_state():
    #setup param for lambda function
    client = boto3.client('ssm')
    client.put_parameter(Name=SUMO_SSM_NAME, Type='SecureString', Value='https://httpstat.us/200', KeyId='alias/aws/ssm')

    # run lambda function
    response = lambda_function.handle_state(SUMO_SSM_NAME, MESSAGE)

    # test response
    assert response.get("status") == "success"

@mock_ssm
def test_handle_state_invalid_message():
    #setup param for lambda function
    client = boto3.client('ssm')
    client.put_parameter(Name=SUMO_SSM_NAME, Type='SecureString', Value='https://httpstat.us/200', KeyId='alias/aws/ssm')

    # run lambda function
    with pytest.raises(TypeError):
        response = lambda_function.handle_state(SUMO_SSM_NAME, ['not', 'a', 'string'])

@mock_ssm
def test_handle_state_failed_post():
    #setup failed POST param for lambda function
    client = boto3.client('ssm')
    client.put_parameter(Name=SUMO_SSM_NAME, Type='SecureString', Value='https://httpstat.us/403', KeyId='alias/aws/ssm')

    # run lambda function
    with pytest.raises(exceptions.ConnectionError):
        response = lambda_function.handle_state(SUMO_SSM_NAME, MESSAGE)
