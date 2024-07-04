from flask import Flask


app = Flask(__name__)

from .Admin import auth

# Registering blueprints
app.register_blueprint(admin.admin_bp)