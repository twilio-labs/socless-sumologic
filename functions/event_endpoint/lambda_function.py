import simplejson as json, os
from socless import create_events
from datetime import datetime


EVENTS_TABLE = os.environ.get('SOCLESS_EVENTS_TABLE')
PLAYBOOKS_TABLE = os.environ.get('SOCLESS_PLAYBOOKS_TABLE')

def lambda_handler(event, context):
    ingest = json.loads(event['body'])

    if isinstance(ingest['details'], str):
        ingest['details'] = json.loads(ingest['details'])

    event_data = {}
    event_data['event_type'] = ingest.get('name')
    event_data['data_types'] = ingest.get('data_types')
    event_data['event_meta'] = ingest.get('event_meta')
    event_data['playbook'] = ingest.get('playbook')
    event_data['dedup_keys'] = ingest.get('dedup_keys')
    event_data['details'] = ingest.get('details')
    resp = create_events(event_data, context)
    if not resp.get('status'):
        return {"statusCode": 200, "body": json.dumps(resp.get('message'))}
    return {"statusCode": 200}
