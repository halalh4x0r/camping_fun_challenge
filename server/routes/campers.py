from flask import Blueprint, request, jsonify
from server import db
from server.models import Camper

campers_bp = Blueprint('campers', __name__)

@campers_bp.route('', methods=['GET'])
def get_campers():
    campers = Camper.query.all()
    return jsonify([camper.to_dict() for camper in campers])

@campers_bp.route('/<int:id>', methods=['GET'])
def get_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({'error': 'Camper not found'}), 404
    
    return jsonify(camper.to_dict(include_signups=True))

@campers_bp.route('', methods=['POST'])
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

@campers_bp.route('/<int:id>', methods=['PATCH'])
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