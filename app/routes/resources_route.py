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
    description = data.get('description')
    resource_type = data.get('type')

    # Handle file upload
    file = request.files['file']

    # Save file to Supabase storage in 'resources' bucket
    if file:
        filename = file.filename
        file_path = f"resources/{filename}"  # Storing in 'resources' bucket
        file.save(file_path)

        # Get Supabase storage URL
        response = supabase.storage.from_storage(file_path).upload(file_path, file.stream)

        if response.status_code == 200:
            resource_url = f"{supabase.storage_url}/public/{file_path}"
            
            # Update Supabase table with resource information
            resource_data = {'title': title, 'description': description, 'type': resource_type, 'link': resource_url}
            supabase.table('resources').insert(resource_data).execute()

            return jsonify({'message': 'Resource uploaded successfully', 'link': resource_url}), 200
        else:
            return jsonify({'error': 'Failed to upload file to Supabase storage'}), 500
    else:
        return jsonify({'error': 'No file provided in the request'}), 400