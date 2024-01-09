from flask import Blueprint, request, jsonify
import re
import os
from app.utils.database import connect_to_supabase
import base64

resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/')
def authhello():
    return jsonify({'message': 'accessing resources service test 1', 'errors': ['hello']}), 400

@resources_bp.route('/add', methods=['POST'])
def save_resource():
     return jsonify({'message': 'access with success '}), 400


@resources_bp.route('/test', methods=['POST'])
def test():

    supabase = connect_to_supabase()

    data = request.form
    
    title = data.get('title')
    description= data.get('description')
    type = data.get('type')
    user_id = data.get('user_id')
    
    resource_data = {'title': title, 'description': description, 'type': type, 'user_id': user_id}
    supabase.table('resources').insert(resource_data).execute()

    
    return jsonify({
            'result': 'record registered  '
        }), 200