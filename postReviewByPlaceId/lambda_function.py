import json
import boto3
import uuid
import decimal
import datetime

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0 or o % 1 < 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
        
dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    payload = json.loads(event['body'])
    review_id = str(uuid.uuid4())
    
    requiredParams = [
        'author', 'review'
        ]
    
    missingParams = False
    
    for i in requiredParams:
        if payload.get(i) == None:
            missingParams = True
    
    if missingParams == True:
        statusCode = 400
        body = json.dumps("Missing request parameters")
    else:
        now = datetime.datetime.now()   
        newItem={
            'author': payload["author"],
            'place_id': event["pathParameters"]["place_id"],
            'review_id': review_id,
            'rating': payload["rating"],
            'review': payload["review"],
            'date_time': str(now)
        }
    table = dynamodb.Table("placeReviewsTable")
    response = table.put_item(
        Item = newItem
        )
        
    statusCode=200
    body = json.dumps(newItem, cls=DecimalEncoder)
    
    return {
        'statusCode': statusCode,
        'body': body
    }
