import json
import boto3

dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    payload = json.loads(event["body"])
    newItem={
            'author': payload["author"],
            'place_id': event["pathParameters"]["place_id"],
            'rating': "0",
            'formatted_address': payload["formatted_address"],
            'latitude': payload['latitude'],
            'longitude': payload['longitude'],
            'place_name': payload['place_name'],
            'weekday_text': payload['weekday_text']
        }
    table = dynamodb.Table("placesTable")
    response = table.put_item(
        Item = newItem
        )
    return {
        'statusCode': 200,
        'body': json.dumps(newItem)
    }
