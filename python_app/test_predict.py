import sys
from app import create_app
from app.ml_model import predict

app = create_app()

with app.app_context():
    try:
        result = predict(usia=25, lama_rawat=5, jenis_kelamin='L')
        print("Prediction result:", result)
    except Exception as e:
        import traceback
        traceback.print_exc()
