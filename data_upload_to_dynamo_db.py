
# Gets the existing table using dynamodb_resource.Table('ImageRecognitionResults')
# Puts 3 items into the table simulating cleaned Rekognition results:

# dog.jpg — labels: ['dog', 'animal', 'pet'], confidence: 98.5
# cat.jpg — labels: ['cat', 'animal', 'feline'], confidence: 95.2
# car.jpg — labels: ['car', 'vehicle', 'transport'], confidence: 91.7


# Each item should have a timestamp and status: 'processed'
# Print f"{image_id} saved successfully!" for each one
# Proper try/except throughout

from datetime import datetime, timezone
import boto3

animals = [
    {'dog.jpg': {
    'confidence': 98.5,
    'labels': ['dog', 'animal', 'pet']}},
    {'cat.jpg': {
    'confidence': 95.2,
    'labels': ['cat', 'animal', 'feline']}},
    {'car.jpg': {
    'confidence': 91.7,
    'labels': ['car', 'vehicle', 'transport']}}
]

table = boto3.resource('dynamodb', region_name='us-east-1').Table('ImageRecognitionResults')
print(table)

number_of_animal_in_animals = len(animals)
i=0

while i<number_of_animal_in_animals:
    for key, value in animals[i].items():
        image_id = key
        labels = value['labels']
        confidence =int(value['confidence'])
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        status = 'processed'

        try:
            table.put_item(
                Item={
                    'Image_Id': image_id,
                    'Timestamp': timestamp,
                    'Labels': labels,
                    'Confidence': confidence,
                    'Status': status
                }
            )
            print(f'{image_id} saved successfully!')
        except Exception as e:
            print(f'Error: {e}')
    i+=1

