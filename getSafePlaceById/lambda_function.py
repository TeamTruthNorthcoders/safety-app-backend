import json
import boto3

dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    table = dynamodb.Table("testPlaces2")
    # place_id = 'ChIJ0VTAWfCue0gRFM2lcIaciFY' 
    place_id = event["pathParameters"]["place_id"]
    response = table.get_item(
        Key = {"place_id":place_id}
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
    
