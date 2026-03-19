import os, json
from datetime import datetime, timezone, timedelta

os.environ["ENVIRONMENT"] = "production"
os.environ["ALERT_THRESHOLD"] = "80"
os.environ["RETENTION_DAYS"] = "7"

event = {
    "body": '{"metrics": [{"server": "web-01", "cpu": 92, "memory": 75, "recorded_at": "2026-03-17 10:00:00"}, {"server": "web-02", "cpu": 45, "memory": 85, "recorded_at": "2026-03-15 08:00:00"}, {"server": "db-01", "cpu": 78, "memory": 95, "recorded_at": "2026-03-09 12:00:00"}, {"server": "db-02", "cpu": 30, "memory": 40, "recorded_at": "2026-03-17 09:00:00"}]}'
}

# Reads all 3 env vars
# Filters metrics recorded within RETENTION_DAYS
# From those, flags servers where cpu OR memory exceeds ALERT_THRESHOLD
# Returns {server: {"cpu": val, "memory": val, "alert": "cpu"/"memory"/"both"}} — use "both" if both exceed threshold
# Response message: "production: 2 servers flagged"
# Proper structure throughout

environment = os.environ.get("ENVIRONMENT", "development")
alert_threshold = int(os.environ.get("ALERT_THRESHOLD", 80))
retention_period = int(os.environ.get("RETENTION_DAYS", 7))

def lambda_handeler( events , context ):
    try:
        phrased_json = json.loads(events.get('body',''))

        metrics = phrased_json.get('metrics', [])

        retention_date = datetime.now(timezone.utc) - timedelta(days=retention_period)

        filtered_metrics = [ metric for metric in metrics if metric.get('recorded_at')>retention_date.strftime('%Y-%m-%d %H:%M:%S')]


        flagged_servers = [ server for server in filtered_metrics if (server.get('cpu')>alert_threshold or server.get('memory')>alert_threshold) or (server.get('cpu')>alert_threshold and server.get('memory')>alert_threshold)]

        return{
            "statusCode": 200,
            "body": json.dumps(
                {
                    'message':f'{environment}: {len(flagged_servers)} servers flagged'
                },indent=2
            )
        }
    
    except Exception as e:
        print(e)
        return{
            'statusCode': 500,
            'body': str('Error on server')
        }

print(lambda_handeler(event, None))