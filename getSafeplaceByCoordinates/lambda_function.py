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
    coords = event["pathParameters"]["coordinates"]
    if len(coords.split(",")) == 2):
        getUrlByCoords = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + coords + "&key=AIzaSyDbrLDnVEOkT-UDzkM8ahFE44X0z13qnh8"
        res = requests.get(getUrlByCoords)
        json_res = json.loads(res.text)
        place_id = json_res['results'][0]["place_id"]
        
        getUrlByPlaceId = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=AIzaSyDbrLDnVEOkT-UDzkM8ahFE44X0z13qnh8"
        res = requests.get(getUrlByPlaceId)
        json_res = json.loads(res.text)
        place_data = json_res['result']

        Item = {}
        Item["formatted_address"] = place_data["formatted_address"]
        Item["latitude"] = place_data["geometry"]["location"]["lat"]
        Item["longitude"] = place_data["geometry"]["location"]["lng"]
        Item["place_name"] = place_data["name"]
        Item["place_id"] = place_id
        if "opening_hours" in place_data:
            Item["weekday_text"] = place_data["opening_hours"]["weekday_text"]
        else:
            Item["weekday_text"] = ["No opening times given"]
            
        statusCode=200
        body = json.dumps(Item, cls=DecimalEncoder)
    else:
        statusCode=402,
        body=json.dumps("Coordinates must be in ':lat,:lng' format, eg.'53.4704767,-2.2394124'")


    
    return {
        'statusCode': statusCode,
        'body':body
    }