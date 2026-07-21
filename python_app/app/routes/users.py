"""
User Management Routes
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import User, LogAktivitas
from app import db
from app.decorators import admin_required
from datetime import datetime
from werkzeug.security import generate_password_hash

users_bp = Blueprint('users', __name__)

@users_bp.route('/')
@login_required
@admin_required
def index():
    """List pengguna"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    role_filter = request.args.get('role', '')
    
    query = User.query
    
    if search:
        query = query.filter(
            db.or_(
                User.nama_lengkap.ilike(f'%{search}%'),
                User.username.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        )
    
    if role_filter:
        query = query.filter(User.role == role_filter)
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('users/index.html', users=users, search=search, role_filter=role_filter)

@users_bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    """Tambah pengguna baru"""
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            nama_lengkap = request.form.get('nama_lengkap')
            email = request.form.get('email')
            role = request.form.get('role')
            
            # Validasi
            if User.query.filter_by(username=username).first():
                flash('Username sudah digunakan!', 'danger')
                return redirect(url_for('users.create'))
            
            # Hash password
            hashed_password = generate_password_hash(password)
            
            # Create user
            user = User(
                username=username,
                password=hashed_password,
                nama_lengkap=nama_lengkap,
                email=email,
                role=role,
                status='aktif'
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Log aktivitas
            log = LogAktivitas(
                user_id=current_user.id,
                aksi='CREATE_USER',
                deskripsi=f'Menambah pengguna baru: {username}',
                ip_address=request.remote_addr
            )
            db.session.add(log)
            db.session.commit()
            
            flash('Pengguna berhasil ditambahkan!', 'success')
            return redirect(url_for('users.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal menambahkan pengguna: {str(e)}', 'danger')
    
    return render_template('users/create.html')

@users_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    """Edit pengguna"""
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            new_role = request.form.get('role')
            new_status = request.form.get('status')
            
            # Cegah admin mengubah role/status diri sendiri
            if user.id == current_user.id:
                if new_role and new_role != 'admin':
                    flash('Tidak dapat mengubah role Anda sendiri!', 'danger')
                    return render_template('users/edit.html', user=user)
                if new_status and new_status != 'aktif':
                    flash('Tidak dapat menonaktifkan akun Anda sendiri!', 'danger')
                    return render_template('users/edit.html', user=user)
            
            user.nama_lengkap = request.form.get('nama_lengkap')
            user.email = request.form.get('email')
            user.role = new_role
            user.status = new_status
            
            # Update password jika diisi
            new_password = request.form.get('password')
            if new_password:
                user.password = generate_password_hash(new_password)
            
            user.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Log aktivitas
            log = LogAktivitas(
                user_id=current_user.id,
                aksi='UPDATE_USER',
                deskripsi=f'Mengubah data pengguna: {user.username}',
                ip_address=request.remote_addr
            )
            db.session.add(log)
            db.session.commit()
            
            flash('Data pengguna berhasil diperbarui!', 'success')
            return redirect(url_for('users.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui pengguna: {str(e)}', 'danger')
    
    return render_template('users/edit.html', user=user)

@users_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete(id):
    """Hapus pengguna"""
    if id == current_user.id:
        return jsonify({'status': 'error', 'message': 'Tidak dapat menghapus akun sendiri!'}), 400
    
    try:
        user = User.query.get_or_404(id)
        username = user.username
        
        db.session.delete(user)
        db.session.commit()
        
        # Log aktivitas
        log = LogAktivitas(
            user_id=current_user.id,
            aksi='DELETE_USER',
            deskripsi=f'Menghapus pengguna: {username}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Pengguna berhasil dihapus!'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@users_bp.route('/view/<int:id>')
@login_required
@admin_required
def view(id):
    """Detail pengguna"""
    user = User.query.get_or_404(id)
    
    # Get log aktivitas user
    logs = LogAktivitas.query.filter_by(user_id=id).order_by(
        LogAktivitas.created_at.desc()
    ).limit(10).all()
    
    return render_template('users/view.html', user=user, logs=logs)
