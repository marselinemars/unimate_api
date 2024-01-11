from flask import Blueprint, request, jsonify
from app.utils.database import connect_to_supabase

resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/')
def authhello():
    return jsonify({'message': 'accessing resources service test 1', 'errors': ['hello']}), 400

@resources_bp.route('/uploadResource', methods=['POST'])
def uploadResource():
    supabase = connect_to_supabase()

    data = request.form

    title = data.get('title')
    description = data.get('description')
    resource_type = data.get('type')
    user_id = data.get('user_id')

    # Handle file uploads
    files = request.files.getlist('files')

    if files:
        resource_data = {'title': title, 'description': description, 'type': resource_type, 'user_id': user_id}
        resource_record = supabase.table('resources').insert(resource_data).execute()

        resource_id = resource_record['data'][0]['id']

        attachments = []

        for file in files:
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
            attachment_url = supabase.storage.from_('resources').get_public_url(file_path)

            # Store the attachment in the new database table
            attachment_data = {'resource_id': resource_id, 'attachment_url': attachment_url}
            supabase.table('resource_attachments').insert(attachment_data).execute()

            attachments.append({'attachment_url': attachment_url})

        resource_data['attachments'] = attachments

        return jsonify(resource_data), 200
    else:
        return jsonify({'error': 'No files provided in the request'}), 400
