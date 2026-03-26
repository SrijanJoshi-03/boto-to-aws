



import boto3    
from decimal import Decimal


client = boto3.client('dynamodb', region_name='us-east-1')
dynamo_db = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamo_db.Table('practiceTable-001')
try:
    client.transact_write_items(
        TransactItems =[
            {
            "Put": {
                "TableName": "practiceTable-001",
                "Item": {
                    'image_id': {"S":'newdog.jpg'},
                    'timeStamp': {"S": '2026-03-20T10:00:00'},
                    'status': {"S": 'processed'},
                }}},
            {"Update": {
                "TableName": "practiceTable-001",
                "Key": {
                    'image_id': {"S": 'cat.jpg'},
                    'timeStamp': {"S": '2026-03-19T08:05:00'}
                    },
                "UpdateExpression" : "Set #st = :s ",
                "ExpressionAttributeNames": {'#st':'status'},
                "ExpressionAttributeValues": {':s':{"S":'archived'}},
                }}
                ])
    response = table.scan()
    items = response.get("Items",[])
    for item in items:
        print(f"Image ID: {item.get('image_id')}, Status: {item.get('status')}")


except Exception as e:
    print(f"Full error: {e}")
    if hasattr(e, 'response'):
        print(f"Cancellation reasons: {e.response['CancellationReasons']}")

