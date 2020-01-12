import json
import boto3

dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    payload = json.loads(event["body"])
    
    requiredParams = [
        'author', 'formatted_address', 'latitude', 'longitude', 'place_name', 'weekday_text'
        ]
    
    missingParams = False
    
    for i in requiredParams:
        if payload.get(i) == None:
            missingParams = True
    
    if missingParams == True:
        statusCode = 400
        body = json.dumps("Missing request parameters")
    else:
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
            
        statusCode=200
        body = json.dumps(newItem)
    
    return {
        'statusCode': statusCode,
        'body': body
    }