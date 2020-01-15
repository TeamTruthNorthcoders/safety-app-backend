import json
import boto3
import decimal
from botocore.vendored import requests

dynamodb = boto3.resource("dynamodb")

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0 or o % 1 < 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    print(event)
    payload = json.loads(event["body"])
    
    requiredParams = [
        'author']
        # , 'formatted_address', 'latitude', 'longitude', 'place_name', 'weekday_text'
        # ]
    

    missingParams = False
    
    for i in requiredParams:
        if payload.get(i) == None:
            missingParams = True
    
<<<<<<< HEAD
    if missingParams == True:
=======
    if "rating_value" not in json.loads(event["body"]):
>>>>>>> 88f1270bfd772c226c1a37aa8987420f016e671d
        statusCode = 400
        body = json.dumps("Missing request parameters")
    else:
<<<<<<< HEAD
        url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + event["pathParameters"]["place_id"] + "&key=AIzaSyDbrLDnVEOkT-UDzkM8ahFE44X0z13qnh8"
        res = requests.get(url)
        google_results = json.loads(res.text)['result']

        
        newItem = {
            'place_id': event["pathParameters"]["place_id"],
            "formatted_address" : google_results["formatted_address"],
            "latitude" : decimal.Decimal(str(google_results["geometry"]["location"]["lat"])),
            "longitude" : decimal.Decimal(str(google_results["geometry"]["location"]["lng"])),
            "place_name" :google_results["name"],
            "author" : payload["author"],
            'rating': 0,
           'rating_count':0
           }
        if "opening_hours" in google_results:
            newItem["weekday_text"] = google_results["opening_hours"]["weekday_text"]
        else:
            newItem["weekday_text"] = ["No opening times given"]

    
        # newItem={
        #         'author': payload["author"],
        #         'place_id': event["pathParameters"]["place_id"],
        #         'rating': 0,
        #         'formatted_address': payload["formatted_address"],
        #         'latitude': decimal.Decimal(str(payload['latitude'])),
        #         'longitude': decimal.Decimal(str(payload['longitude'])),
        #         'place_name': payload['place_name'],
        #         'weekday_text': payload['weekday_text']
        #     }

        table = dynamodb.Table("safeplaceTable")
        response = table.put_item(
            Item = newItem
            )
=======
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
>>>>>>> 88f1270bfd772c226c1a37aa8987420f016e671d
        
        statusCode=200
        body = json.dumps(newItem, cls=DecimalEncoder)
    
    return {
        'statusCode': statusCode,
        'body': body
    }