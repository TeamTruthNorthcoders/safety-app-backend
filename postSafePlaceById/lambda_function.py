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
    
    if missingParams == True:
        statusCode = 400
        body = json.dumps("Missing request parameters")
    else:
        url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + event[git pull ori   "pathParameters"]["place_id"] + "&key=AIzaSyDbrLDnVEOkT-UDzkM8ahFE44X0z13qnh8"
        res = requests.get(url)
        google_results = json.loads(res.text)['result']

        
        newItem = {
            'place_id': event["pathParameters"]["place_id"],
            "formatted_address" : google_results["formatted_address"],
            "latitude" : decimal.Decimal(str(google_results["geometry"]["location"]["lat"])),
            "longitude" : decimal.Decimal(str(google_results["geometry"]["location"]["lng"])),
            "place_name" :google_results["name"],
            "author" : payload["author"],
            'rating': 0
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
        
        statusCode=200
        body = json.dumps(newItem, cls=DecimalEncoder)
    
    return {
        'statusCode': statusCode,
        'body': body
    }