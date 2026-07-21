import sys
from app import create_app

app = create_app()

with app.test_client() as client:
    # Need to simulate a logged-in user or just bypass login_required
    # Let's bypass login_required by disabling it in config for this test
    app.config['LOGIN_DISABLED'] = True
    
    try:
        response = client.post('/perhitungan/hitung')
        print("Status code:", response.status_code)
        if response.status_code != 200:
            print("Error data:", response.data.decode('utf-8'))
    except Exception as e:
        import traceback
        traceback.print_exc()
