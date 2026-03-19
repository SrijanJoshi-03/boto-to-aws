
# Creates a bucket called aizen-logs-{today's date} using datetime e.g. aizen-logs-2026-03-17
# Uploads 3 log files with put_object:

# Key: logs/2026-03-15.log, Body: "server started"
# Key: logs/2026-03-16.log, Body: "backup completed"
# Key: logs/2026-03-17.log, Body: "server stopped"


# Lists only files inside the logs/ folder
# Reads and prints the content of the most recent log file
# Cleans up — deletes all files and the bucket
# Proper try/except and f-strings throughout
import boto3
from datetime import datetime,timezone,timedelta

s3= boto3.client('s3')

date_today = datetime.now(timezone.utc)

bucket_name = f"aizen-logs-{date_today.strftime('%Y-%m-%d')}"

def lambda_handeler( key,body ):
    try:
        s3.create_bucket(Bucket=bucket_name)
        for object_name,object_value in zip(key,body):
            s3.put_object(Bucket=bucket_name, Key=object_name, Body=object_value)
        for object_name in key:
            date_in_logs = datetime.strptime(object_name, 'logs/%Y-%m-%d.log')
            if date_today.date() == date_in_logs.date():
                print(s3.get_object(Bucket=bucket_name, Key=object_name)['Body'].read().decode('utf-8'))
            s3.delete_object(Bucket=bucket_name, Key=object_name)
        s3.delete_bucket(Bucket=bucket_name)    
        print(f"sucessfully deleted {bucket_name}")
    except Exception as e:
        return{
            "statusCode": 500,
            'error': str(e)
        }
print(lambda_handeler(['logs/2026-03-15.log','logs/2026-03-16.log','logs/2026-03-17.log'] , ["server started","backup completed","server stopped"]))