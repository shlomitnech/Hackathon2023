Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import json
... import boto3
... import time
... 
... def lambda_handler(event, context):
...     client = boto3.client('rekognition')
... 
...     # Start the label detection job
...     response = client.start_label_detection(
...         Video={'S3Object': {'Bucket': 'traffic-cars', 'Name': 'realVid.mp4'}},
...         MinConfidence=50,
...         JobTag='video-label-detection'
...     )
...     job_id = response['JobId']
... 
...     # Poll the status of the label detection job
...     while True:
...         job_response = client.get_label_detection(JobId=job_id)
... 
...         # Check if the job is complete
...         if job_response['JobStatus'] in ['SUCCEEDED', 'FAILED']:
...             break
... 
...         # Wait for a few seconds before checking the status again
...         time.sleep(5)
... 
...     # Get the label detection results
...     result_response = client.get_label_detection(JobId=job_id)
... 
...     # Save the JSON response to an S3 bucket
...     s3_client = boto3.client('s3')
...     s3_client.put_object(
...         Body=json.dumps(result_response, indent=4),
...         Bucket='traffic-cars',
...         Key='videoResponse.json'
...     )
... 
...     return {
        'statusCode': 200,
        'body': json.dumps("Success!")
    }
