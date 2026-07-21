"""
Authentication Routes
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, LogAktivitas
from app import db
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Halaman login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username dan password harus diisi!', 'danger')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(username=username, status='aktif').first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.now()
            
            # Log aktivitas
            log = LogAktivitas(
                user_id=user.id,
                aksi='Login',
                deskripsi='Login berhasil',
                ip_address=request.remote_addr
            )
            db.session.add(log)
            db.session.commit()
            
            flash(f'Selamat datang, {user.nama_lengkap}!', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Username atau password salah!', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout"""
    # Log aktivitas
    log = LogAktivitas(
        user_id=current_user.id,
        aksi='Logout',
        deskripsi='Logout dari sistem',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('auth.login'))
