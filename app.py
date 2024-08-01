from flask import Flask, render_template, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Import and register the blueprints for authentication, administration, user, and guest
from Admin.auth import auth_bp
from Admin.admin import admin_bp
from User.user import user_bp
from Guest.guest import guest_app

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'toto123'
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(guest_app, url_prefix='/guest')


# Sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
