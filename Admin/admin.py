from functools import wraps

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash
from config import get_db


admin_bp = Blueprint('admin', __name__)


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/register', methods=['POST'])
@admin_required
def admin_register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    password = generate_password_hash(password)
    if not username or not password or not role:
        return jsonify({'message': 'Missing username, password, or role'}), 400

    conn = get_db()
    cur = conn.cursor()

    if role == 'admin':
        return jsonify({'message': 'Admin Creation not available'}), 400
    elif role == 'user':
        try:
            cur.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                        (username, password, role))
            conn.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except psycopg2.Error as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({'message': 'Role must be user'}), 400


@admin_bp.route('/ApprovePrompt/<int:prompt_id>', methods=['PUT'])
@admin_required
def approve_prompt(prompt_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("""
            UPDATE prompts
            SET status = 'validated'
            WHERE id = %s
            RETURNING content;
        """, (prompt_id,))
        approved_prompt = cur.fetchone()
        conn.commit()

        if approved_prompt is None:
            return jsonify({'message': 'Prompt not found or not in en waiting status'}), 404

        return jsonify({'message': f'Prompt {prompt_id} approved and moved to prompts table'}), 200
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@admin_bp.route('/RejectPrompt/<int:prompt_id>', methods=['PUT'])
@admin_required
def reject_prompt(prompt_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("UPDATE prompts SET status = 'rejected' WHERE id = %s RETURNING content", (prompt_id,))
        rejected_prompt = cur.fetchone()
        if rejected_prompt is None:
            return jsonify({'message': 'Prompt not found or already processed'}), 404

        conn.commit()
        return jsonify({'message': f'Prompt {prompt_id} rejected and status updated in temp_prompts table'}), 200
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()
