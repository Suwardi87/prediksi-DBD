import sys
from app import create_app

app = create_app()

with app.test_client() as client:
    app.config['LOGIN_DISABLED'] = True
    
    try:
        response = client.post('/training/start', json={'n_estimators': 5})
        print("Status code:", response.status_code)
        if response.status_code != 200:
            print("Error data:", response.data.decode('utf-8'))
    except Exception as e:
        import traceback
        traceback.print_exc()
