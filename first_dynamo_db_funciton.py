import boto3
import json
# Creates the ImageRecognitionResults table using boto3.resource
# Waits until the table exists
# Prints f"Table {table_name} is ready!"
# Wraps everything in try/except

table_name= 'ImageRecognitionResults'
try:
    dynamodb_resource = boto3.resource('dynamodb',region_name='us-east-1')
    table = dynamodb_resource.create_table(
        TableName = table_name,
        KeySchema = [
            {"AttributeName": "Image_Id", "KeyType": "HASH"},
            {"AttributeName": "Timestamp", "KeyType": "RANGE"}
        ],
        AttributeDefinitions = [
            {"AttributeName": "Image_Id" , "AttributeType": "S" },
            {"AttributeName": "Timestamp" , "AttributeType": "S" }
        ],
        BillingMode = "PAY_PER_REQUEST"
    )
    table.wait_until_exists()
    print({
        "statusCode" : 200,
        "body" : json.dumps(f"Table {table_name} is ready!")    
    })
    
except Exception as e:
    print({
        "statusCode" : 500,
        "body" : str(f"Error: {e}")
    })


