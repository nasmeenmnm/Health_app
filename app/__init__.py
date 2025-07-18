from flask import Flask
from flask_login import LoginManager
from .utils import get_user_by_id  # This returns a User instance already

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super-secret-key-123'

    from .routes import main
    from .auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)  

    return app
