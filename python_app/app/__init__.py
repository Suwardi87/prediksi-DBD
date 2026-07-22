"""
Flask Application Factory
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Configuration
    app.config['SECRET_KEY'] = 'dbd-prediction-secret-key-2025'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Database: env var > MySQL > SQLite fallback
    db_url = os.environ.get('DATABASE_URL', '')
    if not db_url:
        try:
            import pymysql
            conn = pymysql.connect(host='localhost', user='root', password='')
            conn.close()
            db_url = 'mysql+pymysql://root:@localhost/db_prediksi_dbd'
        except Exception:
            db_path = os.path.join(os.path.dirname(__file__), '..', 'db.sqlite3')
            db_url = f'sqlite:///{os.path.abspath(db_path)}'

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url

    if 'mysql' in db_url:
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_recycle': 300,
            'pool_pre_ping': True
        }
    else:
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'
    login_manager.login_message_category = 'warning'
    
    # User loader for Flask-Login
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    # Register blueprints
    from app.routes import main_bp
    from app.routes.auth import auth_bp
    from app.routes.data import data_bp
    from app.routes.users import users_bp
    from app.routes.training import training_bp
    from app.routes.prediksi import prediksi_bp
    from app.routes.evaluasi import evaluasi_bp
    from app.routes.perhitungan import perhitungan_bp
    from app.routes.api import api_bp
    from app.routes.laporan import laporan_bp
    from app.routes.log import log_bp
    from app.routes.data_uji import data_uji_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(data_bp, url_prefix='/data')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(training_bp, url_prefix='/training')
    app.register_blueprint(prediksi_bp, url_prefix='/prediksi')
    app.register_blueprint(evaluasi_bp, url_prefix='/evaluasi')
    app.register_blueprint(perhitungan_bp, url_prefix='/perhitungan')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(laporan_bp, url_prefix='/laporan')
    app.register_blueprint(log_bp, url_prefix='/log')
    app.register_blueprint(data_uji_bp, url_prefix='/data_uji')
    # Error handlers
    @app.errorhandler(403)
    def forbidden(e):
        from flask import render_template
        return render_template('403.html'), 403
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            # Ignore if tables already exist
            pass
    
    return app
