from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import psycopg2
import psycopg2.extras

user_bp = Blueprint('user_bp', __name__)

# Configuration de la base de données PostgreSQL
DB_HOST = 'localhost'
DB_NAME = 'PromptDB'
DB_USER = 'postgres'
DB_PASS = 'Toto123'

def get_db():
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

def user_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] != 'user':
            return jsonify({'message': 'user access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@user_bp.route('/AddPrompt', methods=['POST'])
@user_required
def ajouter_prompt():
    data = request.get_json()
    content = data.get('content')
    status = "en attente"

    if not content:
        return jsonify({'message': 'Missing content'}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("INSERT INTO prompts (content, status, user_id) VALUES (%s, %s, %s) RETURNING content",
                    (content, status, get_jwt_identity()['id']))
        prompt = cur.fetchone()
        conn.commit()

        return jsonify({'message': prompt['content']}), 201
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


@user_bp.route('/AlterPrompt', methods=['POST'])
@user_required
def alter_prompt():
    data = request.get_json()
    content = data.get('content')
    status = "en attente"

    if not content:
        return jsonify({'message': 'Missing content'}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("ALTER TABLE prompts (content, status, user_id) VALUES (%s, %s, %s) RETURNING content",
                    (content, status, get_jwt_identity()['id']))
        prompt = cur.fetchone()
        conn.commit()

        return jsonify({'message': prompt['content']}), 201
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()
