from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__)

# Configuration de la base de données PostgreSQL
DB_HOST = 'localhost'
DB_NAME = 'PromptDB'
DB_USER = 'postgres'
DB_PASS = 'Toto123'

def get_db():
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        print(current_user)
        if current_user['role'] != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/register', methods=['POST'])
@admin_required
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({'message': 'Missing username, password, or role'}), 400

    conn = get_db()
    cur = conn.cursor()

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
