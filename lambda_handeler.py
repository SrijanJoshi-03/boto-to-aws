# # Extract the image name from the S3 event
# # Simulate cleaned Rekognition results
# # Save the results to DynamoDB using put_item
# # Check if the same image was processed before using query
# # If processed before, update the existing record's status to 'reprocessed'
# # Return a proper 200 response with the saved data
# # Return 500 if anything goes wrong

import boto3, json
from datetime import datetime, timezone
from decimal import Decimal
from boto3.dynamodb.conditions import Key

dynamo_db = boto3.resource('dynamodb')
table=dynamo_db.Table('practiceTable-001')

def get_rekognition_results(image_name):
    return {
        'dog.jpg': {'labels': ['dog', 'animal', 'pet'], 'confidence': Decimal('98.5')},
        'cat.jpg': {'labels': ['cat', 'animal', 'feline'], 'confidence': Decimal('95.2')},
        'car.jpg': {'labels': ['car', 'vehicle', 'transport'], 'confidence': Decimal('91.7')},
    }.get(image_name, {'labels': ['unknown'], 'confidence': Decimal('0.0')})

event = {
    "Records": [{
        "s3": {
            "bucket": {"name": "my-images-bucket"},
            "object": {"key": "dog.jpg"}
        }
    }]
}

def lambda_handler(event, context):
    try:
        uploaded_image_in_s3_bucket = event.get('Records',[])[0].get('s3', {}).get('object', {}).get('key', '')
        #print(uploaded_image_in_s3_bucket)

        rekognition_result = get_rekognition_results(uploaded_image_in_s3_bucket)
        #print(rekognition_result)

        response = table.query(
            KeyConditionExpression=Key('image_id').eq(uploaded_image_in_s3_bucket)
        )
        items= response.get('Items',[])
        #print(items)
        if items:
            table.update_item(
                Key ={
                    'image_id': uploaded_image_in_s3_bucket,
                    'timeStamp': items[0].get('timeStamp', '')
                },
                UpdateExpression = 'SET #st = :s',
                ExpressionAttributeNames={
                    '#st': 'status'
                },
                ExpressionAttributeValues={
                    ':s': 'reprocessed',
                }
            )
            return{
                    'statusCode': 200,
                    'body':{
                        'message': f'image {uploaded_image_in_s3_bucket} has been process already',
                        'data': rekognition_result
                    }
                }
        else:
            table.put_item(Item={
                'image_id': uploaded_image_in_s3_bucket,
                'timeStamp': datetime.now(timezone.utc).isoformat(),
                'confidence': rekognition_result.get('confidence',''),
                'labels': rekognition_result.get('labels', [] ),
                'status': 'processed'
            })
            return{
                'statusCode': 200,
                'body': {
                    'message': f'image {uploaded_image_in_s3_bucket} processed and saved to dynamodb',
                    'data': rekognition_result
                }
            }


    except Exception as e:
        print(str(e))
        return {
            'statusCode': 500,
            'body': str('Error processing the image')
        }


print(lambda_handler(event, None))

