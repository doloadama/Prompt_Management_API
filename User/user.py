from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import psycopg2
import psycopg2.extras
from functools import wraps
from config import get_db


user_bp = Blueprint('user_bp', __name__)


def user_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] != 'user':
            return jsonify({'message': 'User access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@user_bp.route('/AddPrompt', methods=['POST'])
@user_required
def add_prompt():
    data = request.get_json()
    content = data.get('content')
    status = "en attente"

    if not content:
        return jsonify({'message': 'Missing content'}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("INSERT INTO temp_prompts (content, status, user_id) VALUES (%s, %s, %s) RETURNING content",
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

@user_bp.route('/EditPrompt/<int:prompt_id>', methods=['PUT'])
@user_required
def edit_prompt(prompt_id):
    data = request.get_json()
    content = data.get('content')
    status = "en attente"

    if not content:
        return jsonify({'message': 'Missing content'}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("UPDATE temp_prompts SET content = %s, status = %s WHERE id = %s AND user_id = %s RETURNING content",
                    (content, status, prompt_id, get_jwt_identity()['id']))
        updated_prompt = cur.fetchone()
        if updated_prompt is None:
            return jsonify({'message': 'Prompt not found or not authorized to edit'}), 404

        conn.commit()
        return jsonify({'message': updated_prompt['content']}), 200
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@user_bp.route('/VotePrompt/<int:prompt_id>', methods=['PUT'])
@user_required
def vote_prompt(prompt_id):
    data = request.get_json()
    vote_status = data.get('vote_status')

    if not vote_status or vote_status not in ["en attente", "activer", "rappel", "A supprimer"]:
        return jsonify({'message': 'Invalid vote status'}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("UPDATE temp_prompts SET status = %s WHERE id = %s",
                    (vote_status, prompt_id))
        conn.commit()

        return jsonify({'message': f'Voted {vote_status} on prompt {prompt_id}'}), 200
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@user_bp.route('/Display_all_Prompt', methods=['GET'])
@user_required
def display_prompt_all():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute('SELECT id, content FROM prompts')
        prompts = cur.fetchall()


        return jsonify({'prompts': prompts}), 200

    except Exception as e:
        # Gestion des erreurs
        return jsonify({'error': str(e)}), 500

    finally:
        # Assurez-vous de fermer le curseur et la connexion
        cur.close()
        conn.close()

@user_bp.route('/DisplayPrompt/<int:prompt_id>', methods=['GET'])
@user_required
def display_prompt(prompt_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute('SELECT * FROM prompts')
        prompts = cur.fetchall()


        return jsonify({'prompts': prompts}), 200

    except Exception as e:
        # Gestion des erreurs
        return jsonify({'error': str(e)}), 500

    finally:
        # Assurez-vous de fermer le curseur et la connexion
        cur.close()
        conn.close()