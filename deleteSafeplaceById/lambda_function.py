import json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table("testPlaces2")
    place_id = event["pathParameters"]["place_id"]
    table.delete_item(
    Key={
        'place_id': place_id
    }
    )
    return {
        'statusCode': 204
    }
