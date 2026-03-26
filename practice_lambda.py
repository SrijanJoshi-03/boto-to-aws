from datetime import datetime,timezone
import boto3,json,os
from decimal import Decimal


s3= boto3.client('s3')
dynamo_db = boto3.resource('dynamodb', region_name='us-east-1')
client = boto3.client('rekognition', region_name='us-east-1')


def lambda_handler(event,context):
    try:
        Records=event.get('Records',[])
        for record in Records:
            prased_json = json.loads(record.get('body', '{}'))
            bucket_name = prased_json.get('detail',{}).get('bucket',{}).get('name','')
            object_key = prased_json.get('detail', {}).get('object', {}).get('key', '')

            if not bucket_name or not object_key:
                print("Invalid event structure")
                continue
            
            response_from_rekogniton=client.detect_labels(
                Image={
                    'S3Object': {
                        'Bucket': bucket_name,
                        'Name': object_key
                    }
                }
            )
            lables = response_from_rekogniton.get('Labels')
            if lables:
                table = dynamo_db.Table(os.environ['DYNAMODB_TABLE_NAME'])
                for label in lables:
                    table.put_item(
                        Item={
                            'image-id': f"{object_key}",
                            'timestamp': f"{datetime.now(timezone.utc).isoformat()}{label['Name']}",
                            'confidence': Decimal(str(label['Confidence'])),
                            'label': label['Name'],
                            'status': 'processed'
                        }
                    )
        return{
            "statusCode" : 200,
            "body": json.dumps({
                "message": "Labels detected and stored successfully"
            })
            }
    except Exception as e:
        print(f"Error: {e}")
        return{
            "statusCode" : 500,
            "body": json.dumps({
                "message": "Internal server error"
            })
        }    









