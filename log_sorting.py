import json
from datetime import datetime, timezone, timedelta

body = '{"events": [{"id": "ev1", "name": "server_start", "created_at": "2026-03-17 08:00:00"}, {"id": "ev2", "name": "server_stop", "created_at": "2026-03-10 12:00:00"}, {"id": "ev3", "name": "backup_start", "created_at": "2026-03-16 09:00:00"}, {"id": "ev4", "name": "backup_complete", "created_at": "2026-02-28 14:00:00"}]}'
# Parse it and return only events from the last 10 days, sorted by created_at most recent first, just the event names in that order.

date_10_days_ago = datetime.now(timezone.utc)+timedelta(days=-10)

phrased_json = json.loads(body)

filtered_events = [ event for event in phrased_json.get('events',[]) if event.get('created_at', '') > date_10_days_ago.strftime('%Y-%m-%d %H:%M:%S')]

sorted_events = sorted(filtered_events, key=lambda x: x['created_at'], reverse=True)

sorted_events_by_name = [ event.get('id','') for event in sorted_events]

print(sorted_events_by_name)