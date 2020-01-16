# safety-app-backend

This api was build by using Amazon Web Services. The API is build using API Gateway, which triggers Lambda functions that queries DynamoDB tables.
It provides the backend for an app directing users who might find themselves in potentially unsafe or uncomfortable situations when in Manchester to safe places near them. 

The api can be accessed [here](https://2aw2ojaww1.execute-api.eu-west-2.amazonaws.com/api)


### Endpoints: 

Endpoint                           | Request | Input | Returns                                                                                                                                                                                                                                                                                                                                                  |
| ---------------------------------- | ------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /api/safeplaces               | GET   |  | Gets all currently open safe places from the database. Returns <code>"Items": [ <br> {<br>  "place_name": "Archie's - Burgers Shakes Waffles", <br> "formatted_address": "115 Oxford Rd, Manchester M1 7DU, UK", <br> "place_id": "ChIJMXjRNJOxe0gRtTdRSVb6rb8", <br> "rating": 0,<br> "rating_count": 0, <br> "longitude": -2.2374638, <br> "weekday_text": [ <br> "Monday: 11:00 AM – 2:30 AM", <br> "Tuesday: 11:00 AM – 2:30 AM", <br> "Wednesday: 11:00 AM – 2:30 AM", <br> "Thursday: 11:00 AM – 2:30 AM", <br> "Friday: 11:00 AM – 2:30 AM", <br> "Saturday: 11:00 AM – 3:00 AM", <br> "Sunday: 1:00 PM – 2:00 AM" <br> ], <br> "latitude": 53.47094209999999, <br> "author": "snakeyBoi" <br>}, {...} <code>|                                                                                                                                                       |
| /api/safeplaces/{place_id}    | GET   | place ID as path parameter | <code>"Item": {<br>  "place_name": "Archie's - Burgers Shakes Waffles", <br> "formatted_address": "115 Oxford Rd, Manchester M1 7DU, UK", <br> "place_id": "ChIJMXjRNJOxe0gRtTdRSVb6rb8", <br> "rating": 0,<br> "rating_count": 0, <br> "longitude": -2.2374638, <br> "weekday_text": [ <br> "Monday: 11:00 AM – 2:30 AM", <br> "Tuesday: 11:00 AM – 2:30 AM", <br> "Wednesday: 11:00 AM – 2:30 AM", <br> "Thursday: 11:00 AM – 2:30 AM", <br> "Friday: 11:00 AM – 2:30 AM", <br> "Saturday: 11:00 AM – 3:00 AM", <br> "Sunday: 1:00 PM – 2:00 AM" <br> ], <br> "latitude": 53.47094209999999, <br> "author": "snakeyBoi" <br>}</code>|                                                                                                                                                       |
| /api/safeplaces/{place_id}    | POST  | place ID as path parameter, <code> { "author": "bob"}| Returns the posted safeplace |                                                                                                                                                      
| /api/safeplaces/{place_id}    | PATCH  | place ID as path parameter, <br> <code>{"rating_value": 1}</code>  | Returns the patched place. {<br>  "place_name": "Archie's - Burgers Shakes Waffles", <br> "formatted_address": "115 Oxford Rd, Manchester M1 7DU, UK", <br> "place_id": "ChIJMXjRNJOxe0gRtTdRSVb6rb8", <br> "rating": 0,<br> "rating_count": 0, <br> "longitude": -2.2374638, <br> "latitude": 53.47094209999999, <br> "author": "snakeyBoi" <br>} </code>|                                                                                                                                                       |
| /api/safeplaces/{place_id}    | DELETE  | place ID as path parameter | Returns 204. |                                                                                                                                                       |
| /api/safeplaces/{place_id}/reviews   | GET  | place ID as path parameter  | Returns all reviews for a place. <code>"Items": <br>[ <br>{<br>"place_id": "ChIJ0VTAWfCue0gRFM2lcIaciFY",<br>"rating": 5,<br>"review_id": 1,<br>"author": "NotWeirdo",<br>"body": "Was really safe" <br> }<br>...<br>]</code>|                                                                                                                                                       |
| /api/safeplaces/{place_id}/reviews   | POST  | place ID as path parameter,<br><code>{<br>"author": "person",<br>"review": "this is a good place",<br>"rating": 4<br>} | Returns the posted review. <code>{<br>"place_id": "ChIJ0VTAWfCue0gRFM2lcIaciFY",<br>"review_id": "0a16454f-1ef5-4f32-98c1-82255beff330", <br>"author": "person"}</code>|                                                                                                                                                       |
| /api/reviews/{review_id}    | GET   | review ID as path parameter | Returns the specfied review. <code>{<br>"rating": 5,<br> "review_id": "0a16454f-1ef5-4f32-98c1-82255beff330", <br>"place_id": "abcdef12345", <br>"body": "super safe", <br>"author": "me"<br>}</code>|                                                                                                                                                       |                                                                                                                                                    
| /api/reviews/{review_id}    | DELETE   | review ID as path parameter | Returns 204.| 
