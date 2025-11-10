from flask import Blueprint, request, jsonify
from server import db
from server.models import Signup

signups_bp = Blueprint('signups', __name__)

@signups_bp.route('', methods=['POST'])
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