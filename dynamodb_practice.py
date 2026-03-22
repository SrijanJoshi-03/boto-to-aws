import boto3, json
from boto3.dynamodb.conditions import Key

dynamo_db = boto3.resource('dynamodb', region_name='us-east-1')
table_name = 'practice_dynamoDB_table-001'

s3 = boto3.client('s3')
bucket_name = 'practice-boto3-upload-001033043'

try:
    table = dynamo_db.create_table(
        TableName = table_name,
        KeySchema = [
            {"AttributeName": "image_id", 'KeyType': 'HASH'},
            {"AttributeName": "timestamp", "KeyType": "RANGE"}
        ],
        AttributeDefinitions =[
            {"AttributeName": 'image_id', "AttributeType": "S" },
            {"AttributeName": "timestamp", "AttributeType": "S"}
        ],
        BillingMode = "PAY_PER_REQUEST"
    )
    table.wait_until_exists()
    print(f"{table_name} created successfully")
except Exception as e:
    print(f"Error creating table: {e}")

table = dynamo_db.Table(table_name)
try:
    table.put_item(
        Item={
            "image_id": "test_image_0001",
            "timestamp": "2022-06-02",
            "decription": "second day in australia",
            "location": "redfern,sydney"
        }
    )
    print('item has been uploaded to db succesfully.')
except Exception as e:
    print(f"Error putting item: {e}")

try:
    response = table.query(
        KeyConditionExpression = Key('image_id').eq('test_image_0001') #& Key(
            # 'timestamp').eq('2022-06-02')
    )
    items = response.get('Items',[])
    for item in items:
        print(f'file_name: {item.get('image_id','')},image description: {item.get('description', '')}, image_captured: {item.get('timestamp','')}, image captured point: {item.get('location','')}')
except Exception as e:
    print(f"Error quering items: {e}")

try:
    table.delete()
    table.wait_until_not_exists()
    print(f'{table_name} has been deleted succesfully. ')
except Exception as e:
    print(f"Error deleting table: {e}")



try:
    s3.create_bucket(Bucket=bucket_name)
    print(f'{bucket_name} created successfully')
except Exception as e:
    print(f"Error creating bucket: {e}")    

try:
    s3.put_object(
        Bucket = bucket_name,
        Key = 'testfile.txt',
        Body = f"this is test file uploded fform vs code to the se bucket {bucket_name}"
    )
    print('file uploaded successfully')
except Exception as e:
    print(f"Error uploading file: {e}")

try:
    response = s3.list_objects_v2(Bucket=bucket_name)
    items = response.get('Contents',[])
    for item in items:
        print(item.get('Key',''))
except Exception as e:
    print(f"Error listing objects: {e}")

try:
    response = s3.get_object(
        Bucket = bucket_name,
        Key = 'testfile.txt'
    )
    print(response['Body'].read().decode('utf-8'))
except Exception as e:
    print(f'error : {e}')

try:
    s3.delete_object(
        Bucket = bucket_name,
        Key = 'testfile.txt'
    )
    print('file deleted successfully')
    s3.delete_bucket(Bucket=bucket_name)  
    print(f'{bucket_name} deleted successfully')  
except Exception as e:
    print(f"Error deleting file: {e}")