import json
import boto3
from boto3.dynamodb.conditions import Attr
import decimal
import re 
from datetime import datetime


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0 or o % 1 < 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
        
dynamodb = boto3.resource("dynamodb")

def time_parse(time):
    if (time == "12:00"):
        time = time + " PM"
    return datetime.strptime(time,'%I:%M %p')
    
def check_open(opening_time,closing_time,current_time):
    if opening_time < closing_time:
        return current_time >= opening_time and current_time <= closing_time
    else:
        return current_time >= opening_time or current_time <= closing_time

def filter_places(places):
    filtered_list =[]
    now_date = datetime.now()
    weekday = now_date.weekday()
    now_time = now_date.strftime("%I:%M %p")


    for place in places:
        if ("No opening times given" not in place["weekday_text"]):
            opening_times = place["weekday_text"][weekday]
            if ("Closed" not in opening_times):
                opening_times = re.findall("(\d\d{0,1}){1}(:\d\d{0,1}){0,1}(\sAM|\sPM){0,1}",opening_times)
                opening_time = time_parse("".join(opening_times[0]))
                closing_time = time_parse("".join(opening_times[1]))
                current_time = time_parse(str(now_time))
                
                if (check_open(opening_time,closing_time,current_time)):
                    filtered_list.append(place)
    
    return filtered_list
    
def lambda_handler(event, context):

    try: 
        table = dynamodb.Table("safeplaceTable")
        
        if event["queryStringParameters"] is not None: 
            author = event["queryStringParameters"]["author"]
            response = table.scan(
                FilterExpression=Attr('author').contains(author)
            )
        else:
            response = table.scan()
            
        statusCode = 200
        
        filtered_place_list = {
        "Items" : filter_places(response["Items"])
        }

    except:
        statusCode = 500
 
    if statusCode == 200:
        body = json.dumps(filtered_place_list, cls=DecimalEncoder)
    elif statusCode == 500:
        body = "Internal Server Error"
    else:
        body = "Unknown Error"
    
    return {
        'statusCode': statusCode,
        'body': body
    }