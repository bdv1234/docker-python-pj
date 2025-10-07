from flask import Flask
from .config import Config
from .models import db
from .views import api_bp
from .metrics import register_metrics
from .tasks import make_celery

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(api_bp)

    register_metrics(app)

    # Initialize Celery with app config
    make_celery(app)

    return app