Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import json
... import boto3
... 
... def lambda_handler(event, context):
...     client = boto3.client('rekognition')
...     
...     response = client.detect_labels(
...         Image={"S3Object": {"Bucket": "traffic-cars", "Name": "realImage.jpg"}},
...         MaxLabels= 15,
...         MinConfidence=50
...     )
...     
...     # Save the JSON response to an S3 bucket
...     s3_client = boto3.client('s3')
...     s3_client.put_object(
...         Body=json.dumps(response, indent=4),
...         Bucket='traffic-cars',
...         Key='REAL.json'
...     )
...     
...     return {
...         'statusCode': 200,
...         'body': json.dumps("Complete!")
...     }
