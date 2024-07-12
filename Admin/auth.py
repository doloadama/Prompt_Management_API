from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import psycopg2
import psycopg2.extras

from config import get_db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user:
            # Vérifiez le mot de passe (ici on suppose que le mot de passe est en clair, vous devriez utiliser un hash)
            if user['password_hash'] == password:
                if user['role'] == 'admin':
                    access_token = create_access_token(identity={'id': user['id'], 'role': user['role']})
                    return jsonify({'access_token': access_token}), 200
                elif user['role'] == 'user':
                    access_token = create_access_token(identity={'id': user['id'], 'role': user['role']})
                    return jsonify({'access_token': access_token}), 200
                else:
                    return jsonify({'message': 'Invalid role'}), 403
            else:
                return jsonify({'message': 'Invalid username or password'}), 401
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("SELECT username, role FROM users WHERE id = %s", (current_user['id'],))
        user = cur.fetchone()

        if user:
            return jsonify({'user': user}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()
