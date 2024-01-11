from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate


csrf=CSRFProtect()
migrate = Migrate() 
def create_app():
    from pkg.models import db
    app = Flask(__name__, instance_relative_config=True, static_folder='static', template_folder='templates')
    app.config.from_pyfile("config.py")

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    return app
    

app = create_app()
from pkg import user_routes, admin_routes 