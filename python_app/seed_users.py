"""
Script untuk menambahkan user default ke database
Jalankan dengan: python seed_users.py
"""
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def seed_users():
    """Tambah user default untuk setiap role"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("  MENAMBAHKAN USER DEFAULT KE DATABASE")
        print("="*60 + "\n")
        
        # Definisi user default
        users_data = [
            {
                'username': 'admin',
                'password': 'admin123',
                'nama_lengkap': 'Administrator',
                'email': 'admin@rsud.go.id',
                'role': 'admin'
            },
            {
                'username': 'petugas',
                'password': 'petugas123',
                'nama_lengkap': 'Petugas Kesehatan',
                'email': 'petugas@rsud.go.id',
                'role': 'petugas'
            }
        ]
        
        created_count = 0
        existing_count = 0
        
        for user_data in users_data:
            # Cek apakah user sudah ada
            existing_user = User.query.filter_by(username=user_data['username']).first()
            
            if existing_user:
                print(f"⏭️  User '{user_data['username']}' sudah ada - SKIP")
                existing_count += 1
            else:
                # Hash password
                hashed_password = generate_password_hash(user_data['password'])
                
                # Create user baru
                new_user = User(
                    username=user_data['username'],
                    password=hashed_password,
                    nama_lengkap=user_data['nama_lengkap'],
                    email=user_data['email'],
                    role=user_data['role'],
                    status='aktif'
                )
                
                db.session.add(new_user)
                print(f"✅ User '{user_data['username']}' berhasil ditambahkan")
                print(f"   - Role: {user_data['role']}")
                print(f"   - Password: {user_data['password']}")
                created_count += 1
        
        # Commit semua perubahan
        if created_count > 0:
            db.session.commit()
            print(f"\n✅ Berhasil menambahkan {created_count} user baru")
        
        if existing_count > 0:
            print(f"ℹ️  {existing_count} user sudah ada sebelumnya")
        
        # Tampilkan summary
        print("\n" + "="*60)
        print("  KREDENSIAL LOGIN")
        print("="*60)
        print("\n📋 ADMINISTRATOR:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n👨‍💻 PETUGAS:")
        print("   Username: petugas")
        print("   Password: petugas123")
        print("\n" + "="*60)
        print("⚠️  PENTING: Ubah password default setelah login pertama!")
        print("="*60 + "\n")
        
        # Tampilkan total user
        total_users = User.query.count()
        print(f"📊 Total user di database: {total_users}")
        print()

if __name__ == '__main__':
    seed_users()
