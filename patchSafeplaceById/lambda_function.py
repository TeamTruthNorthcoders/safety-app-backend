import boto3
import json
import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
        
        
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('safeplaceTable')

def lambda_handler(event, context):
    inc_rating = int(json.dumps(json.loads(event["body"])["inc_votes"]))
    
    response = table.update_item(
        Key={
        "place_id": event["pathParameters"]["place_id"]
        },
    UpdateExpression="SET rating = :new_rating",
    ExpressionAttributeValues={
        ':new_rating': inc_rating
    },
    ReturnValues="ALL_NEW"
    )
    return {
        "statusCode": 200,
        "body": json.dumps(response["Attributes"], indent=4, cls=DecimalEncoder)
    }