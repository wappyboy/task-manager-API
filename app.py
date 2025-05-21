from flask import Flask
from config import Config
from database import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # <-- import here

# Initialize app
app = Flask(__name__)
app.config.from_object(Config)

CORS(app)  # <-- enable CORS here

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Register routes
from routes.auth import auth_bp
from routes.tasks import tasks_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(tasks_bp, url_prefix="/api/tasks")

# Create tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
