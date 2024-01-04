from flask import Blueprint, request, jsonify
import re
import os
from app.utils.database import connect_to_supabase
import base64

resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/add', methods=['POST'])
def save_resource():
    supabase = connect_to_supabase()
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        resource_type = data.get('type')
        attachment_data = data.get('attachment')  # Assuming attachment_data is a base64 encoded string

        # Decode base64 and save the file to Supabase Storage
        file_data = base64.b64decode(attachment_data)
        file_name = f"{title}_{resource_type}.{attachment_data.split('/')[1].split(';')[0]}"
        file_path = os.path.join('/tmp', file_name)  # Assuming a temporary directory for file storage

        with open(file_path, 'wb') as file:
            file.write(file_data)

        # Upload the file to Supabase Storage
        storage_response = supabase.storage.from_filename(file_path, f"resources/{file_name}").upload()

        if storage_response['status'] != 200:
            return jsonify({'error': 'Failed to upload file to Supabase Storage'}), 500

        # Get the URL of the uploaded file
        file_url = storage_response['data']['url']

        # Insert the link to the file in the 'resources' table in Supabase
        response = supabase.table('resources').insert([
            {'title': title, 'description': description, 'type': resource_type, 'attachment': file_url}
        ]).execute()

        if response['status'] == 201:
            return jsonify({'message': 'Resource saved successfully'}), 201
        else:
            return jsonify({'error': 'Failed to save resource'}), 500

    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
