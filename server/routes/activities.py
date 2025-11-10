from flask import Blueprint, request, jsonify
from server import db
from server.models import Activity

activities_bp = Blueprint('activities', __name__)

@activities_bp.route('', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities])

@activities_bp.route('/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404
    
    db.session.delete(activity)
    db.session.commit()
    
    return '', 204