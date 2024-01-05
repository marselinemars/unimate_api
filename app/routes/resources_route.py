from flask import Blueprint, request, jsonify
import re
import os
from app.utils.database import connect_to_supabase
import base64

resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/')
def authhello():
    return jsonify({'message': 'accessing resources service', 'errors': ['hello']}), 400

@resources_bp.route('/add', methods=['POST'])
def save_resource():
     return jsonify({'message': 'access with success '}), 400