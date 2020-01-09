import json
import boto3
import uuid

dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    payload = json.loads(event["body"])
    review_id = str(uuid.uuid4())
    newItem={
            'author': payload["author"],
            'place_id': event["pathParameters"]["place_id"],
            'review_id': review_id,
            'rating': 0,
            'body': payload["review"]
        }
    table = dynamodb.Table("placeReviews")
    response = table.put_item(
        Item = newItem
        )
    return {
        'statusCode': 200,
        'body': json.dumps(newItem)
    }
