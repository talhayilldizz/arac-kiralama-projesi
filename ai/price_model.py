import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

try:
    df = pd.read_csv('ai/arac_kira_verisi.csv')
except FileNotFoundError:
    print("Hata: 'arac_kira_verisi.csv' bulunamadı.")
    exit()

if 'id' in df.columns:
    df.drop('id',axis=1)

categorical=[
    'marka',
    'model',
    'hasar_durumu'
]
numerical=[
    'km',
    'model_yili'
]

encoders={}
scaler=StandardScaler()

for col in categorical:
    le=LabelEncoder()
    df[col]=le.fit_transform(df[col])
    encoders[col]=le

df[numerical]=scaler.fit_transform(df[numerical])


X=df.drop('fiyat',axis=1)
y=df['fiyat']

X_train,X_test,y_train,y_test=train_test_split(
    X,y,
    test_size=0.2,
    random_state=42
)

model_rf=RandomForestRegressor(n_estimators=100,random_state=42)
model_rf.fit(X_train,y_train)

y_pred=model_rf.predict(X_test)

mse=mean_squared_error(y_test,y_pred)
rmse=np.sqrt(mse)

print(f"MSE: {mse}")
print(f"RMSE: {rmse:.2f}")

#Modeli kaydedelim

kaydedilecek_dosya={
    "model":model_rf,
    "encoders":encoders,
    "scaler":scaler,
    "categorical_cols":categorical,
    "numerical_cols":numerical
}
joblib.dump(kaydedilecek_dosya, "ai/arac_tahmin_modeli.pkl")