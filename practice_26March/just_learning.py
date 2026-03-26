import boto3, json, os
from boto3.dynamodb.conditions import Key,Attr

s3 = boto3.client('s3') # creating a connection to s3 service using my AWS cerdentials.

dynamodb = boto3.resource('dynamodb') # creating a connection to dynamodb service using my AWS credentials.

os.environ["Environment"] = "Practice"
os.environ["Bucket_Name"] = "helloworld003r4834"
os.environ["Table_Name"] = "Servers"

def env_variables_reader(): #defining a function to get that returns the stored environment varible in the execution context.
    try: # helps to catch error in the code.
        environment = os.environ['Environment']
        bucket_name = os.environ['Bucket_Name']
        table_name = os.environ['Table_Name']

        return [environment,bucket_name,table_name]
    except Exception as e: # helps to catch error in the code.
        print(str(e))

env_variables = env_variables_reader() # calls the env_variable_reader fucniton and stores the values.

def lambda_handler( events, context ): #defining our lambda function.
    try:

        environment = env_variables[0]
        bucket_name = env_variables[1]
        table_name = env_variables[2]

        s3.create_bucket(Bucket=bucket_name) # creates a bucket in s3 with the name stored in the environment variable.
        print(f's3 bucket {bucket_name} has been succesfully created.\n')

        s3.put_object( # uploads the object in the previously created s3 bucket.
            Bucket=bucket_name,
            Key='hello_world.txt',
            Body='Hello World'
        )

        print(f"the file has been uploaded succesfully to {bucket_name}.\n")

        response_from_s3 = s3.list_objects_v2(  # lists all the objects in the bucket and keeps the value in this variable
            Bucket = bucket_name
        )
        Items =response_from_s3.get('Contents',[]) #responce returned by s3 is a dictionary object the data we need is in Content which is a LIST object.
        for item in Items:
            print(f'{item.get("Key")}') # prints the file name that are inside of the s3 bucket.

        response_from_s3_for_object_body = s3.get_object (
            Bucket = bucket_name,
            Key = 'hello_world.txt'
        )
        contents = response_from_s3_for_object_body['Body'].read().decode('utf-8') # reads the body of the file in the s3 bucket.
        print(f'the data inside hello_world.txt is {contents}.\n')

        s3.delete_object( # deletes the object from the s3 bucket.
            Bucket = bucket_name,
            Key = 'hello_world.txt'
        )
        print(f'object has been deleted form the s3 bucket {bucket_name}.\n')

        s3.delete_bucket( # deletes the bucket that was created earlier.
            Bucket = bucket_name
        )
        return{
            "statusCode": 200,
            "body": json.dumps(
                {
                    'message': f'{environment}: bucket {bucket_name} has been created and deleted successfully.'
                }
            )
        }
    except Exception as e: #handels the error without thorowing error on your face.
        return{
            'statusCode': 500,
            'body': json.dumps({
                'message': str(e)
            })
        }

print(lambda_handler('','')) #calls the lambda_handeler funciton to see the result.


def lambda_handler_for_dynamo_db ( events, context ):
    try:
        environment = env_variables[0]
        bucket_name = env_variables[1]
        table_name = env_variables[2]

        table = dynamodb.create_table( # creates a table in the dynamodb.
            TableName = table_name,
            KeySchema = [ # defines Partition key attribute name and Sort Key attribute name
                {"AttributeName":"server_id", "KeyType": "HASH"},
                {"AttributeName":"server_name", "KeyType": "RANGE"} 
            ],

            AttributeDefinitions = [
                {"AttributeName":"server_id", "AttributeType": "S"},
                {"AttributeName":"server_name", "AttributeType": "S"}
            ],
            BillingMode = "PAY_PER_REQUEST"
        )
        table.wait_until_exists() # wait until the table exists in dynamodb.
        print(f'table {table_name} has been succesfully created. \n')

        table.put_item( # puts this item with PK, SK and following attributes in the table
            Item={
                "server_id" : "1",
                "server_name" : "frontend_server",
                "server_type" : "t2.micro",
                "server_status" : "running"
            }
        )
        print('item has been added to the table. \n')

        response = table.query( # queries the table based on the partition key and sort key.
            KeyConditionExpression=Key('server_id').eq("1") & Key('server_name').eq('frontend_server')
        )
        items = response.get("Items",[])
        for item in items:
            print(f'server_id ={item.get("server_id")}, server_name ={item.get("server_name")}, server_type ={item.get("server_type")}, server_status ={item.get("server_status")}')

        table.update_item( # updates this particcular value in the table.
            Key ={
                'server_id' : "1",
                'server_name' : "frontend_server"
            },
            UpdateExpression="SET #status = :val1",
            ExpressionAttributeNames={"#status":"server_status"},
            ExpressionAttributeValues={':val1':'stopped'}
        )
        response2 = table.query( # queries the table based on the partition key and sort key.
            KeyConditionExpression=Key('server_id').eq("1") & Key('server_name').eq('frontend_server')
        )
        items2 = response2.get("Items",[])
        for item2 in items2:
            print(f'server_id ={item2.get("server_id")}, server_name ={item2.get("server_name")}, server_type ={item2.get("server_type")}, server_status ={item2.get("server_status")}')


        table.delete_item( # deletes the item from the table based on the partition key and sort key.
            Key={
                "server_id" : "1",
                "server_name" : "frontend_server"
            }
        )
        print('item has been deleted from the table. \n')

        table.delete() # deletes the table from the dynamodb.
        table.wait_until_not_exists() # waits until the table is deleted from the dynamodb.
        print(f'table {table_name} has been deleted successfully. \n')

        return{
            "statusCode": 200,
            "body": json.dumps(
                {
                    'message': f'{environment}: table {table_name} has been created and deleted successfully.'
                }
            )
        }
    except Exception as e:
        return{
            'statusCode': 500,
            'body': json.dumps({
                'message': str(e)
            })
        }

print(lambda_handler_for_dynamo_db('', ''))