from socless import socless_bootstrap
import requests, boto3

client = boto3.client('ssm')

def handle_state(sumo_ssm_name, message):
   if not isinstance(message, str):
      raise TypeError("'message' argument type should be String, not {}".format(type(message)))
   
   response = client.get_parameter( Name=sumo_ssm_name, WithDecryption=True )
   SUMO_URL = response['Parameter']['Value']

   sumo_response = requests.post(SUMO_URL, data = { 'message' : message } )

   #check for correct response
   if not sumo_response.ok:
      # failure to post response
      raise requests.exceptions.ConnectionError('Failed to post message to SumoLogic. Status Code: {} \n Response: {}'.format(sumo_response.status_code, sumo_response.text))

   return { "status" : "success" }

def lambda_handler(event,context):
   return socless_bootstrap(event,context,handle_state)
