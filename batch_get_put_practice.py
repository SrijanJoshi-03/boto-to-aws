import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('practiceTable-001')

try:
    with table.batch_writer() as batch:
        batch.put_item(Item={
            'image_id': 'elephant.jpg',
            'timeStamp': '2026-03-20T08:00:00',
            'labels': ['elephant', 'animal'],
            'confidence': Decimal('96.0'),
            'status': 'processed'
        })
        batch.put_item(Item={
            'image_id': 'lion.jpg',
            'timeStamp': '2026-03-20T08:05:00',
            'labels': ['lion', 'animal', 'wild'],
            'confidence': Decimal('94.0'),
            'status': 'processed'
        })
        batch.put_item(Item={
            'image_id':'tiger.jpg',
            'timeStamp': '2026-03-20T08:05:00',
            'labels': ['tiger', 'animal', 'wild'],
            'confidence': Decimal('93.5'),
            'status': 'processed'
        })
    
        print('batch items have been uploaded succesfully.')

        response = dynamodb.batch_get_item(
            RequestItems={
                'practiceTable-001': {
                    'Keys': [
                        {'image_id':'elephant.jpg','timeStamp':'2026-03-20T08:00:00'},
                        {'image_id':'lion.jpg','timeStamp':'2026-03-20T08:05:00'}
                    ]
                }
            }
        )
        items= response.get('Responses', {}).get('practiceTable-001', [])
        for item in items:
            print(f'Labels: {item.get('labels',[])}, Confidence: {item.get('confidence', '')}')
except Exception as e:
    print(f"Error in batch operation: {e}")