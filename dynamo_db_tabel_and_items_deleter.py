import boto3
table = boto3.resource('dynamodb', region_name='us-east-1').Table('ImageRecognitionResults')
table.delete()
table.wait_until_not_exists()
print("Table deleted!")
