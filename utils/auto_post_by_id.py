import requests
import json

place_ids = ["ChIJeyO8PJSxe0gR4t_aMX3LVms"]
jsons = {"Items" : []}
root_URL = "https://2aw2ojaww1.execute-api.eu-west-2.amazonaws.com/api/safeplaces/"

for place_id in place_ids:
    url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=AIzaSyDbrLDnVEOkT-UDzkM8ahFE44X0z13qnh8"
    res = requests.get(url)
    json_res = json.loads(res.text)
    item = json_res['result']
    data = {}
    data["formatted_address"] = item["formatted_address"]
    data["latitude"] = item["geometry"]["location"]["lat"]
    data["longitude"] = item["geometry"]["location"]["lng"]
    data["place_name"] = item["name"]
    data["author"] = "snakeyBoi"
    
    if "opening_hours" in item:
        data["weekday_text"] = item["opening_hours"]["weekday_text"]
    else:
        data["weekday_text"] = ["No opening times given"]

    json_data = json.dumps(data)
    res = requests.post(root_URL + place_id,json_data)


    jsons["Items"].append(json_data)
    print(jsons)
with open('./data.json', 'w') as fs:
        json.dump(jsons,fs)

