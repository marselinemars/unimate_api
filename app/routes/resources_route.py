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
    print('a login request ')
    supabase = connect_to_supabase()
    data = request.json

    title = data.get('title')

    
    return jsonify({
            'the sent title is ': title }), 200
    return jsonify( {'title': title, 'description': description, 'type': type, 'user_id': user_id}), 200