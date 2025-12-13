import pandas as pd
import joblib

def fiyat_tahmin_et(arac_bilgileri):
    dosya=joblib.load("ai/arac_tahmin_modeli.pkl")
    model=dosya['model']
    encoders=dosya['encoders']
    scaler=dosya['scaler']

    df=pd.DataFrame([arac_bilgileri])

    for col in dosya['categorical_cols']:
        try:
            df[col] = encoders[col].transform(df[col])
        except ValueError:
            df[col] = 0 

    df[dosya["numerical_cols"]] = scaler.transform(df[dosya["numerical_cols"]])
    
    tahmin = model.predict(df)
    return tahmin[0]