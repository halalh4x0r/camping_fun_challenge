from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import validates

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///camping.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class Camper(db.Model):
    __tablename__ = 'campers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    # Relationships
    signups = db.relationship('Signup', back_populates='camper', cascade='all, delete-orphan')
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Name is required")
        return name.strip()
    
    @validates('age')
    def validate_age(self, key, age):
        age = int(age)
        if age < 8 or age > 18:
            raise ValueError("Age must be between 8 and 18")
        return age
    
    def to_dict(self, include_signups=False):
        data = {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }
        
        if include_signups:
            data['signups'] = [signup.to_dict(include_activity=True) for signup in self.signups]
            
        return data

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    
    # Relationships
    signups = db.relationship('Signup', back_populates='activity', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'difficulty': self.difficulty
        }

class Signup(db.Model):
    __tablename__ = 'signups'
    
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    
    # Foreign keys
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    
    # Relationships
    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')
    
    @validates('time')
    def validate_time(self, key, time):
        time = int(time)
        if time < 0 or time > 23:
            raise ValueError("Time must be between 0 and 23")
        return time
    
    def to_dict(self, include_activity=False, include_camper=False):
        data = {
            'id': self.id,
            'time': self.time,
            'camper_id': self.camper_id,
            'activity_id': self.activity_id
        }
        
        if include_activity:
            data['activity'] = self.activity.to_dict()
            
        if include_camper:
            data['camper'] = self.camper.to_dict()
            
        return data

# Routes
@app.route('/')
def index():
    return {'message': 'Camping Fun API'}

@app.route('/campers', methods=['GET'])
def get_campers():
    campers = Camper.query.all()
    return jsonify([camper.to_dict() for camper in campers])

@app.route('/campers/<int:id>', methods=['GET'])
def get_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({'error': 'Camper not found'}), 404
    
    return jsonify(camper.to_dict(include_signups=True))

@app.route('/campers', methods=['POST'])
def create_camper():
    data = request.get_json()
    
    try:
        camper = Camper(
            name=data.get('name'),
            age=data.get('age')
        )
        
        db.session.add(camper)
        db.session.commit()
        
        return jsonify(camper.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400

@app.route('/campers/<int:id>', methods=['PATCH'])
def update_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({'error': 'Camper not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'name' in data:
            camper.name = data['name']
        if 'age' in data:
            camper.age = data['age']
            
        db.session.commit()
        
        return jsonify(camper.to_dict()), 202
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400

@app.route('/activities', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities])

@app.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404
    
    db.session.delete(activity)
    db.session.commit()
    
    return '', 204

@app.route('/signups', methods=['POST'])
def create_signup():
    data = request.get_json()
    
    try:
        signup = Signup(
            time=data.get('time'),
            camper_id=data.get('camper_id'),
            activity_id=data.get('activity_id')
        )
        
        db.session.add(signup)
        db.session.commit()
        
        return jsonify(signup.to_dict(include_activity=True, include_camper=True)), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)