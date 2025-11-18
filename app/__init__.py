from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

ma = Marshmallow()
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    ma.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.main import bp as main_bp
    from app.clients import bp as clients_bp
    from app.users import bp as users_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(clients_bp, url_prefix='/clients')
    app.register_blueprint(users_bp, url_prefix='/users')
    return app


from app import models