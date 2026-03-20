import boto3,json
from datetime import datetime,timezone
from decimal import Decimal
from boto3.dynamodb.conditions import Key

# items = [
#     {'image_id': 'dog.jpg', 'timestamp': '2026-03-19T08:00:00', 'confidence': Decimal('98.5'), 'labels': ['dog', 'animal', 'pet'], 'status': 'processed'},
#     {'image_id': 'cat.jpg', 'timestamp': '2026-03-19T08:05:00', 'confidence': Decimal('95.2'), 'labels': ['cat', 'animal', 'feline'], 'status': 'processed'},
#     {'image_id': 'car.jpg', 'timestamp': '2026-03-19T08:10:00', 'confidence': Decimal('91.7'), 'labels': ['car', 'vehicle', 'transport'], 'status': 'processed'},
#     {'image_id': 'dog.jpg', 'timestamp': '2026-03-19T09:00:00', 'confidence': Decimal('97.1'), 'labels': ['dog', 'puppy', 'cute'], 'status': 'processed'},
#     {'image_id': 'bird.jpg', 'timestamp': '2026-03-19T09:05:00', 'confidence': Decimal('88.3'), 'labels': ['bird', 'animal', 'flying'], 'status': 'processed'},
# ]

dynamo_db = boto3.resource('dynamodb')

table_name = 'practiceTable-001'

# # try:
# #     table = dynamo_db.create_table(
# #         TableName = table_name,
# #         KeySchema = [
# #             {"AttributeName": "image_id", "KeyType": "HASH"},
# #             {"AttributeName": "timeStamp", "KeyType": "RANGE"}
# #         ],
# #         AttributeDefinitions=[
# #             {"AttributeName":"image_id", "AttributeType":"S"},
# #             {"AttributeName":"timeStamp", "AttributeType":"S"}
# #         ],
# #         BillingMode = "PAY_PER_REQUEST"
# #     )
# #     table.wait_until_exists()
# #     print(f'{table_name} has been created succesfully. Please provide teh data. \n')

# #     for item in items:
# #         table.put_item(Item={
# #             'image_id' : item.get('image_id',''),
# #             'timeStamp': item.get('timestamp',''),
# #             'confidence': item.get('confidence', 0),
# #             'labels': item.get('labels', []),
# #             'status': item.get('status', '')
# #         })
# #         print(f"Item {item['image_id']} added successfully t0 {table_name}.")
# # except Exception as e:
# #     print(str(e))

# table = dynamo_db.Table(table_name)

# try:
#     response = table.query(
#     KeyConditionExpression=Key('image_id').eq('dog.jpg') & Key('timeStamp').between('2026-03-19T07:00:00','2026-03-19T08:30:00')
#     )
#     items = response.get("Items", [])
#     count =0
#     for item in items:
#         count +=1
#         print(f"Confidence : {item.get('confidence', 0)}, labels : {item.get('labels',[])}")
#     print(f'Found {count} results for dog.jpg')

# except Exception as e:
#     print(str(e))

table = dynamo_db.Table(table_name)
table.delete()
table.wait_until_not_exists()
print('table deleted')