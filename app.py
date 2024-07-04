from flask import Flask
from flask_jwt_extended import JWTManager
# Importer et enregistrer les blueprints d'authentification et d'administration
from Admin.auth import auth_bp
from Admin.admin import admin_bp
app = Flask(__name__)

# Configuration JWT
app.config['JWT_SECRET_KEY'] = 'toto123'
jwt = JWTManager(app)


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def index():
    return 'Hello, world!'

if __name__ == '__main__':
    app.run(debug=True)
