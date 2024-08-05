from config import *
from flask import Flask, request, Blueprint, jsonify

guest_app = Blueprint('guest', __name__)

@guest_app.route('/Buy', methods=['GET'])
def buy():
    data = request.get_json()
    id_prompt = data['id_prompt']

    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM prompts WHERE id = %s', (id_prompt,))
