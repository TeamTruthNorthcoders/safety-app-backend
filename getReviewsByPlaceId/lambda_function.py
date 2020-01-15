import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource("dynamodb")

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0 or o % 1 < 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
        
     
def lambda_handler(event, context):
    table = dynamodb.Table("placeReviewsTable")
    place_id = event["pathParameters"]["place_id"]
    fe = Key('place_id').eq(place_id)
    pe = "#author, #rating,#review,#place_id,#review_id,#date_time"
    # Expression Attribute Names for Projection Expression only.
    ean = {
        "#author": "author",
        "#rating": "rating",
        "#review": "review",
        "#place_id":"place_id",
        "#review_id":"review_id",
        "#date_time":"date_time"}
    esk = None

    response = table.scan(
    FilterExpression=fe,
    ProjectionExpression=pe,
    ExpressionAttributeNames=ean
    )
    while 'LastEvaluatedKey' in response:
        response = table.scan(
        ProjectionExpression=pe,
        FilterExpression=fe,
        ExpressionAttributeNames= ean,
        ExclusiveStartKey=response['LastEvaluatedKey']
        )
    if len(response["Items"]) == 0:
        return {
            'statusCode': 200,
            'body': "There are no reviews for this place yet"
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps(response, cls=DecimalEncoder)
        }




