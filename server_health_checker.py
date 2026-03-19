import os
import json

os.environ["ENVIRONMENT"] = "production"
os.environ["THRESHOLD"] = "75"

event = {
    "body": '{"servers": [{"id": "s1", "name": "web-01", "cpu": 85, "memory": 60}, {"id": "s2", "name": "web-02", "cpu": 45, "memory": 90}, {"id": "s3", "name": "db-01", "cpu": 92, "memory": 88}, {"id": "s4", "name": "db-02", "cpu": 30, "memory": 45}]}'
 }
# Reads ENVIRONMENT and THRESHOLD from env vars
# Flags servers where either cpu or memory is above THRESHOLD
# Returns flagged server names and which metric triggered it e.g. {"web-01": "cpu", "web-02": "memory", "db-01": "cpu"}
# Response message: "production: 3 servers flagged"
# Proper try/except, json.loads() inside try, body as json.dumps()
environment = os.environ.get('ENVIRONMENT')
threshold = int(os.environ.get('THRESHOLD'))
def lambda_handeler( events , context ):
    try:
        prased_json= json.loads(events.get('body',{}))
        flagges_servers =[ server for server in prased_json.get('servers',[]) if server.get('cpu',0)>threshold or server.get('memory',0)>threshold]
        result= {i.get('name',''):('cpu' if i.get('cpu', 0)> threshold else 'memory') for i in flagges_servers}
        return{
            'statusCode': 200,
            'body': json.dumps({
                'message': f"{environment}: {len(flagges_servers)} servers flagged",
                'result': result
            },indent=2)
        }
    except Exception as e:
        return{
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
print(lambda_handeler(event, None))