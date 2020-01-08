import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource("dynamodb")

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
        
        
def lambda_handler(event, context):
    table = dynamodb.Table("placeReviews")
    print(event)
    place_id = event["pathParameters"]["place_id"]
    fe = Key('place_id').eq(place_id)
    pe = "#a,#r,#b,#pi, #ri"
    # Expression Attribute Names for Projection Expression only.
    ean = { "#a": "author", "#r": "rating", "#b": "body","#pi":"place_id","#ri":"review_id"}
    esk = None
    

    response = table.scan(
    FilterExpression=fe,
    ProjectionExpression=pe,
    ExpressionAttributeNames=ean
    )

    for i in response['Items']:
     print(json.dumps(i, cls=DecimalEncoder))

    while 'LastEvaluatedKey' in response:
        response = table.scan(
        ProjectionExpression=pe,
        FilterExpression=fe,
        ExpressionAttributeNames= ean,
        ExclusiveStartKey=response['LastEvaluatedKey']
        )

    for i in response['Items']:
        print(json.dumps(i, cls=DecimalEncoder))
        
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }





