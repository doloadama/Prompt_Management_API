from functools import wraps

from flask_jwt_extended import jwt_required, get_jwt_identity

from config import *
from flask import Flask, request, Blueprint, jsonify

guest_app = Blueprint('guest', __name__)




@guest_app.route('/display_prompt/<int:prompt_id>', methods=['GET'])
def display_prompt_guest(keyword):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM prompts WHERE keyword = %s', (keyword,))




