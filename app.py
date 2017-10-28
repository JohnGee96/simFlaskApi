from flask import Flask, abort, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from math import radians, cos, sin, asin, sqrt
import json, flask_restless


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# class Geolocation(db.Model):
#     __tablename__ = "geolocations"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    
#     created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # geolocation = db.relationship(Geolocation, backref=db.backref('geolocations'))
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    lat = db.Column(db.Float(9), nullable=False)
    lng = db.Column(db.Float(9), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(),
                           onupdate=func.now())

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'         : self.id,
           'title'      : self.title,
           'body'       : self.body,
           'lat'        : self.lat,
           'lng'        : self.lng,
           'modified_at': dump_datetime(self.created_at),
           'updated_at' : dump_datetime(self.updated_at)
        #    # This is an example how to deal with Many2Many relations
        #    'many2many'  : self.serialize_many2many
       }

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user/<int:id>')
def show_user_profile(id):
    # show the user profile for that user
    query = User.query.filter_by(id=id).first()
    respJson = json.dumps({'username': query.username, 'email': query.email})
    return respJson

def haversine(lat1,lng1, lat2, lng2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lat1, lng1, lat2, lng2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

def findNearbyPosts(inputJson):
    targetLat = inputJson['lat']
    targetLng = inputJson['lng']
    targetRadius = inputJson['radius']
    resultPosts = []
    posts = Post.query.all()
    for post in posts:
        lat = post.lat
        lng = post.lng
        distance = haversine(targetLat,targetLng,lat,lng)
        if distance < targetRadius:
            resultPosts.append(post)
    return resultPosts

# Expects a JSON with current geolocation and radius in km
# {
#   lat: 51.503364
#   lng:  -0.127625
#   radius: 5
# }
@app.route('/api/nearby_posts', methods=['POST'])
def find_nearby_posts():
    if not request.json:
        abort(400)
    if all (key in request.json for key in ("lat","lng","radius")):
        result = findNearbyPosts(request.json)
    else:
        abort(400)
    return jsonify([p.serialize for p in result])


@app.route('/post/<id>')
def show_post(id):
    post = Post.query.filter_by(id=id).first()
    respJson = json.dumps({'title': post.title, 'body': post.body})
    return respJson

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(User, methods=['GET'])
manager.create_api(Post, methods=['GET','POST', 'DELETE'])

 
