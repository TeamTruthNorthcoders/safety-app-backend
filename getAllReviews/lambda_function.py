import json
import boto3
from boto3.dynamodb.conditions import Attr
import decimal

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
    try: 
        table = dynamodb.Table("placeReviewsTable")
        
        if event["queryStringParameters"] is not None: 
            author = event["queryStringParameters"]["author"]
            response = table.scan(
                FilterExpression=Attr('author').contains(author)
            )
        else:
            response = table.scan()
            
        statusCode = 200
        
    except:
        statusCode = 500
 
    if statusCode == 200:
        body = json.dumps(response, cls=DecimalEncoder)
    elif statusCode == 500:
        body = "Internal Server Error"
    else:
        body = "Unknown Error"
    
    return {
        'statusCode': statusCode,
        'body': body
    }