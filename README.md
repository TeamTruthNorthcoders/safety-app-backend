# safety-app-backend


Endpoints:

POST review by place id 
takes body: 
{
	"author": "person",
	"review": "this is a good place",
	"rating": "4"
}

GET all safeplaces
no arguments needed

GET safeplace by place id
takes place_id "ChIJ0VTAWfCue0gRFM2lcIaciFY" 

GET reviews by place id
takes place_id "ChIJ0VTAWfCue0gRFM2lcIaciFY" 

GET reviews by review id
takes review_id "0a16454f-1ef5-4f32-98c1-82255beff330"
