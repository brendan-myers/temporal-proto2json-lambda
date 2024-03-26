
import boto3
from google.protobuf.json_format import MessageToJson
import os
from temporalio.api.export.v1 import WorkflowExecutions
import uuid
from urllib.parse import unquote_plus

s3_client = boto3.client('s3')

def decode_protobuf(input_path, output_path):
    workflowExecutions = WorkflowExecutions()

    with open(input_path, 'rb') as f:
        data = f.read()
        workflowExecutions.ParseFromString(data)

    outputJson = MessageToJson(workflowExecutions)

    with open(output_path, "w") as o:
        o.write(outputJson)


def lambda_handler(event, context):
    output_bucket = os.environ["S3_TARGET_BUCKET"]

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        upload_path = '/tmp/json-{}'.format(tmpkey)
        
        s3_client.download_file(bucket, key, download_path)
        
        decode_protobuf(download_path, upload_path)

        s3_client.upload_file(upload_path, output_bucket, '{}.json'.format(key))