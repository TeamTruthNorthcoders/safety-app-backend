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
    table = dynamodb.Table("safeplaceTable")
    place_id = event["pathParameters"]["place_id"]
    response = table.get_item(
        Key = {
            "place_id": place_id
        }
        )
        
    if "Item" in response:
        item = response["Item"]
    else:
        return {
            'statusCode': 400,
            'msg': "Place Not Found"
        }
        
    return {
        'statusCode': 200,
        'body': json.dumps(item, cls=DecimalEncoder)
    }
    
