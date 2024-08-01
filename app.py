from flask import Flask, render_template
from flask_jwt_extended import JWTManager
# Importer et enregistrer les blueprints d'authentification et d'administration
from Admin.auth import auth_bp
from Admin.admin import admin_bp
from User.user import user_bp
from Guest.guest import guest_app
app = Flask(__name__)

# Configuration JWT
app.config['JWT_SECRET_KEY'] = 'toto123'
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')

app.register_blueprint(user_bp, url_prefix='/user_bp')

app.register_blueprint(guest_app, url_prefix='/guest')

@app.route('/')
def index():
    """
    A function to display the connexion page of the app
    :return:
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
