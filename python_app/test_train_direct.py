import sys
from app import create_app, db
from app.models import PasienDBD, KasusBulanan
from app.ml_model import prepare_training_data, train_model

app = create_app()

with app.app_context():
    try:
        pasien_list = PasienDBD.query.all()
        kasus_records = KasusBulanan.query.all()
        kasus_bulanan_dict = {(kb.bulan, kb.tahun): kb.jumlah_kasus for kb in kasus_records}
        
        df = prepare_training_data(pasien_list, kasus_bulanan_dict)
        result = train_model(
            df,
            n_estimators=5,
            random_state=42
        )
        print("Training success!")
    except Exception as e:
        import traceback
        traceback.print_exc()
