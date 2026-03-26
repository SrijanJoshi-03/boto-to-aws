import boto3
table = boto3.resource('dynamodb', region_name='us-east-1').Table('Image-recogniton-result')

response =table.scan()
items = response.get('Items',[])
print(items)