import json
import boto3
import decimal

dynamodb = boto3.resource("dynamodb")

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    print(event)
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
                'rating': 0,
                'formatted_address': payload["formatted_address"],
                'latitude': decimal.Decimal(str(payload['latitude'])),
                'longitude': decimal.Decimal(str(payload['longitude'])),
                'place_name': payload['place_name'],
                'weekday_text': payload['weekday_text']
            }

        table = dynamodb.Table("safeplaceTable")
        response = table.put_item(
            Item = newItem
            )
        
        statusCode=200
        body = json.dumps(newItem, cls=DecimalEncoder)
    
    return {
        'statusCode': statusCode,
        'body': body
    }