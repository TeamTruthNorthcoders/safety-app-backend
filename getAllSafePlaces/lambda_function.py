import json
import boto3

dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    table = dynamodb.Table("safeplaceTable")
    response = table.scan()
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
