"""Reset passwords for all users"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    pw_map = {
        'admin': 'admin123',
        'petugas': 'petugas123'
    }
    
    for username, password in pw_map.items():
        user = User.query.filter_by(username=username).first()
        if user:
            user.password = generate_password_hash(password)
            print(f'{username}: password reset to {password}')
        else:
            print(f'{username}: NOT FOUND')
    
    db.session.commit()
    
    # Verify
    for username, password in pw_map.items():
        user = User.query.filter_by(username=username).first()
        if user:
            ok = user.check_password(password)
            print(f'  Verify {username}/{password}: {ok}')
