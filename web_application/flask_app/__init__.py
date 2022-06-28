from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from flask_app.views.main_views import main_bp
    
    app.register_blueprint(main_bp)
    
    return app