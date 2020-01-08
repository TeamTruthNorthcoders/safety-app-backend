import json
import boto3

dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    table = dynamodb.Table("placeReviews")
    # review_id = 'ChIJ0VTAWfCue0gRFM2lcIaciFY' 
    review_id = event["pathParameters"]["review_id"]
    response = table.get_item(
        Key = {"review_id":review_id}
        )
        
    if "Item" in response:
        item = response["Item"]
        # item = "item.....blah blah"
    else:
        return {
            'statusCode': 400,
            'msg': "nahhh"
        }
        
        
        
        
    return {
        'statusCode': 200,
        'body': json.dumps(item),
        # 'event': event["pathParameters"]
    }
    
