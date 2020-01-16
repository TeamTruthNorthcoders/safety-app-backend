import json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table("placeReviewsTable")
    review_id = event["pathParameters"]["review_id"]
    table.delete_item(
    Key={
        'review_id': review_id
    }
    )
    return {
        'statusCode': 204
    }
