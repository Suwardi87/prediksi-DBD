"""
Custom Decorators untuk Role-Based Access Control
"""
from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def role_required(*roles):
    """
    Decorator untuk membatasi akses berdasarkan role user
    
    Usage:
        @role_required('admin')
        @role_required('admin', 'petugas')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Silakan login terlebih dahulu!', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.role not in roles:
                flash('Anda tidak memiliki akses ke halaman ini!', 'danger')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator khusus untuk admin only"""
    return role_required('admin')(f)

def admin_or_petugas_required(f):
    """Decorator untuk admin atau petugas"""
    return role_required('admin', 'petugas')(f)
