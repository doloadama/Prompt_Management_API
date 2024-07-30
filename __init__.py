from flask import Flask

from Admin import admin

app = Flask(__name__)

from .Admin import auth

# Registering blueprints
app.register_blueprint(admin.admin_bp)