import json
import boto3
import decimal
import datetime
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


    payload = json.loads(event["body"])
    
    requiredParams = [
        'author']

    
    missingParams = False
    
    for i in requiredParams:
        if payload.get(i) == None:
            missingParams = True
    
    if missingParams == True:
        statusCode = 400
        body = json.dumps("Missing request parameters")
    else:
        url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + event["pathParameters"]["place_id"] + "&key=AIzaSyDbrLDnVEOkT-UDzkM8ahFE44X0z13qnh8"
        res = requests.get(url)
        google_results = json.loads(res.text)['result']
        now = datetime.datetime.now()   
        newItem = {
            'place_id': event["pathParameters"]["place_id"],
            "formatted_address" : google_results["formatted_address"],
            "latitude" : decimal.Decimal(str(google_results["geometry"]["location"]["lat"])),
            "longitude" : decimal.Decimal(str(google_results["geometry"]["location"]["lng"])),
            "place_name" :google_results["name"],
            "author" : payload["author"],
            'rating': 0,
            'rating_count': 0,
            'date_time': str(now)
        }
        
        if "opening_hours" in google_results:
            newItem["weekday_text"] = google_results["opening_hours"]["weekday_text"]
        else:
            newItem["weekday_text"] = ["No opening times given"]

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