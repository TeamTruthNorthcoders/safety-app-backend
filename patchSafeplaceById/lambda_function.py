import boto3
import json
import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0 or o % 1 < 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
        
        
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('safeplaceTable')

def lambda_handler(event, context):
    
    if "rating_value" not in json.loads(event["body"]):
        statusCode = 400
        body = "Missing request parameter"
    else:
        req_rating_value = int(json.dumps(json.loads(event["body"])["rating_value"]))
        
        response = table.update_item(
            Key={
            "place_id": event["pathParameters"]["place_id"]
            },
        UpdateExpression="SET rating = rating + :req_rating, rating_count = :inc_rating_count + rating_count",
        ExpressionAttributeValues={
             ':inc_rating_count': 1,
            ':req_rating' : req_rating_value
            
        },
        ReturnValues="ALL_NEW"
        )
        patchedItem = {
             "author": response["Attributes"]["formatted_address"],
              "formatted_address": response["Attributes"]["formatted_address"],
              "place_name": response["Attributes"]["place_name"],
              "place_id": response["Attributes"]["place_id"],
              "rating": decimal.Decimal(str(response["Attributes"]["rating"])),
              "rating_count": decimal.Decimal(str(response["Attributes"]["rating_count"])),
              "longitude": decimal.Decimal(str(response["Attributes"]["longitude"])),
              "latitude": decimal.Decimal(str(response["Attributes"]["latitude"])),
        }
        statusCode = 200
        body = json.dumps(patchedItem, cls=DecimalEncoder)
        
    return {
        "statusCode": statusCode,
        "body": body
    }