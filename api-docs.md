# Project Hearound API Documentations

### GET /api/posts
Retrieve all posts. There will be field

{
  "num_results": 4, 
  "objects": [
    {
      "body": "this is the first post", 
      "created_at": "2017-10-23T22:13:07", 
      "id": 1, 
      "lat": 51.503364, 
      "lng": -0.127625, 
      "title": "hello world", 
      "updated_at": "2017-10-23T22:13:07"
    }, 
    {
      "body": "this is another post", 
      "created_at": "2017-10-23T22:40:31", 
      "id": 2, 
      "lat": 51.503364, 
      "lng": -0.127625, 
      "title": "2nd Post", 
      "updated_at": "2017-10-23T22:40:31"
    }, 
    {
      "body": "this is Tufts", 
      "created_at": "2017-10-24T01:21:48", 
      "id": 3, 
      "lat": 42.408705, 
      "lng": -71.119563, 
      "title": "Tufts Location", 
      "updated_at": "2017-10-24T01:21:48"
    }, 
    {
      "body": "this is around Home", 
      "created_at": "2017-10-24T01:24:17", 
      "id": 4, 
      "lat": 42.355567, 
      "lng": -71.152997, 
      "title": "Home Location", 
      "updated_at": "2017-10-24T01:24:17"
    }
  ], 
  "page": 1, 
  "total_pages": 1
}

### GET /api/posts/#
Retrieves a post with id #.

{
  "body": "this is Tufts", 
  "created_at": "2017-10-24T01:21:48", 
  "id": 3, 
  "lat": 42.408705, 
  "lng": -71.119563, 
  "title": "Tufts Location", 
  "updated_at": "2017-10-24T01:21:48"
}

### POST /api/nearby_posts
Retrieve posts within a fixed radius around a geolocation. Must provide a POST request with the following
JSON format:

{
    "lat": 51.503364
    "lng":  -0.127625
    "radius": 5  #in kilometer
}

### Post /api/posts
Create a new post by providing a POST request with following JSON format:

{
    "title": "sample post",
    "body": "This geolocation is also at Tufts", 
    "lat": 42.407371, 
    "lng": -71.119477
}
