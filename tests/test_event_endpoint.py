'''Test event_endpoint'''
# pylint: disable=protected-access
# pylint: disable=wrong-import-position
# pylint: disable=redefined-outer-name
from tests.conftest import * #imports testing boilerplate
from requests import exceptions

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

def test_lambda_handler(event, context):
    #test lambda_handler
    response = lambda_function.lambda_handler(event, context)

    assert response.get("statusCode") == 200