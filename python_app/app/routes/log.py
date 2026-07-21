from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import LogAktivitas
from app.decorators import admin_required

log_bp = Blueprint('log', __name__)

@log_bp.route('/')
@login_required
@admin_required
def index():
    """List log aktivitas"""
    page = request.args.get('page', 1, type=int)
    # Ambil log dari yang terbaru
    logs = LogAktivitas.query.order_by(LogAktivitas.created_at.desc()).paginate(
        page=page, per_page=15, error_out=False
    )
    return render_template('log/index.html', logs=logs)
