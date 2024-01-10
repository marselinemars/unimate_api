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
    file = request.files.get('file')
    

    # Save file to Supabase storage in 'resources' bucket
    if file:
        filename = file.filename
        file_path = f"resources/{filename}"  # Storing in 'resources' bucket
        file_options = {"content-type": file.mimetype}

        # Upload file to Supabase storage
        supabase.storage.from_("resources").upload(
            file=file.read(),
            path=file_path,
            file_options=file_options
        )

        # Get Supabase storage URL
        resource_url = supabase.storage.from_('resources').get_public_url(file_path)

        # Update Supabase table with resource information
        resource_data = {'title': title, 'description': description, 'type': resource_type, 'attachment': resource_url}
        supabase.table('resources').insert(resource_data).execute()

        return jsonify(resource_data), 200
    else:
        return jsonify({'error': 'No file provided in the request'}), 400