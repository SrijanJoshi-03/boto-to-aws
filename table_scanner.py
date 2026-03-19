import boto3
table = boto3.resource('dynamodb', region_name='us-east-1').Table('ImageRecognitionResults')
print(table.scan())
