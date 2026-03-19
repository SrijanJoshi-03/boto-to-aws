import boto3
from datetime import datetime,timezone

files_to_be_uploaded=[ 'localfile.log' , 'localfile.json' , 'server.log' , 'server.json' , 's3.log']
data_for_files = [ 'logs for local file' , 'data for local file stored in json' , 'data for servers stored in log format' , 'data for servers stored in json format' , 's3 bucket logs in log format' ]

s3 = boto3.client("s3")

bucket_name = f'aizen-bucket-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-001'

def lambda_handeler ( object_name , object_value ):
    try:

        s3.create_bucket(Bucket=bucket_name)
        print(f's3 bucket {bucket_name} has been succesfully created.\n')

        for file_name , file_value in zip(object_name,object_value):

            s3.put_object(Bucket=bucket_name , Key=file_name , Body=file_value)

            print(f'{file_name} have been succesfully uploaded to {bucket_name}.\n')


        main_response = s3.list_objects_v2(Bucket=bucket_name)

        files = [object_name.get("Key") for object_name in main_response.get("Contents" , [])]
        print(f'{files}\n')

        log_files =[file for file in files if file.endswith('.log')]
        print(f'{log_files}\n')

        for log_file in log_files:
            response_1 = s3.get_object(Bucket=bucket_name,Key=log_file)
            print(f'[{log_file}]:{response_1["Body"].read().decode("utf-8")}\n')
            s3.delete_object(Bucket=bucket_name, Key=log_file)
            print(f'{files} have been succesfully deleted.\n')
        
        response_for_json_files = s3.list_objects_v2(Bucket=bucket_name)
        json_files = [object_name.get("Key") for object_name in response_for_json_files.get("Contents", [])]
        print(f'{json_files}\n')
        
        for json_file in json_files:
            response_2 = s3.get_object(Bucket=bucket_name,Key=json_file)
            print(f'[{json_file}]:{response_2["Body"].read().decode("utf-8")}\n')
            s3.delete_object(Bucket=bucket_name, Key=json_file)
            print(f'{json_file} have been succesfully deleted.\n')

        s3.delete_bucket(Bucket=bucket_name)
        print(f's3 bucket {bucket_name} has been succesfully deleted.\n')


    except Exception as e:
        if e:
            print(f'Error: {e}')
print(lambda_handeler(files_to_be_uploaded, data_for_files))



