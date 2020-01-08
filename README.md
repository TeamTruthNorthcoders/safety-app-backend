# safety-app-backend


Endpoints:

POST review by place id
takes body: 
```
{
	"author": "person",
	"review": "this is a good place",
	"rating": "4"
}
```
returns : 
```
{
	"place_id": "ChIJ0VTAWfCue0gRFM2lcIaciFY"
	"review_id": "0a16454f-1ef5-4f32-98c1-82255beff330"
	"author": "person",
	"review": "this is a good place",
	"rating": "4"
}
```


GET all safeplaces
no arguments needed
returns :
```
 "Items": [
    {
      "place_id": "ChIJ0VTAWfCue0gRFM2lcIaciFY"
    },
    {
      "place_id": "ChIJB_4uquyxe0gRcLqDm4_2N4k"
    },
    {
      "place_id": "ChIJMXjRNJOxe0gRtTdRSVb6rb8"
    }...
  ]
```

GET safeplace by place id
takes place_id "ChIJ0VTAWfCue0gRFM2lcIaciFY" 
returns : 
```
{
  "place_id": "ChIJ0VTAWfCue0gRFM2lcIaciFY"
}
```

GET reviews by place id
takes place_id "ChIJ0VTAWfCue0gRFM2lcIaciFY" 
returns : 
```
  "Items": [
    {
      "place_id": "ChIJ0VTAWfCue0gRFM2lcIaciFY",
      "rating": "5",
      "review_id": "1",
      "author": "NotWeirdo",
      "body": "Was turbo safe, man"
    }...
  ]
```


GET reviews by review id
takes review_id "0a16454f-1ef5-4f32-98c1-82255beff330"
returns : 
```
{
  "rating": "5",
  "review_id": "0a16454f-1ef5-4f32-98c1-82255beff330",
  "place_id": "abcdef12345",
  "body": "super safe",
  "author": "me"
}
```
