import pandas as pd
import random 
import numpy as np

NUM_SAMPLES=400

araclar={
    'Fiat': ['Egea', 'Egea', 'Egea', 'Linea'], 
    'Renault': ['Clio', 'Clio', 'Megane', 'Symbol'],
    'Toyota': ['Corolla', 'Yaris'],
    'Ford': ['Focus', 'Fiesta'],
    'BMW': ['320i', '520i'], 
    'Mercedes': ['C180', 'A200']
}

marka_agirliklari=[0.35,0.30,0.15,0.10,0.05,0.05]


hasar_durumu={
    'Hasarsız':1.0,
    'Lokal Boyalı':0.95,
    'Değişenli':0.85,
    'Ağır Hasarlı':0.60
}

data=[]

for i in range(1,NUM_SAMPLES+1):
    #Marka model seçimi
    marka=random.choices(
        list(araclar.keys()), 
        weights=marka_agirliklari, 
        k=1
    )[0]
    model=random.choice(araclar[marka])

    #Model yılı seçimi yeni modeller daha az
    yil=random.choices(
        range(2015,2025),
        weights=[1, 2, 3, 4, 5, 5, 4, 3, 2, 1],
        k=1
    )[0]

    #KM yıla bağlı
    yas=2025-yil
    km= int(yas*random.uniform(10000,30000)) + random.randint(0,5000)

    #Hasar durumu
    hasar=random.choices(
        list(hasar_durumu.keys()),
        weights=[0.4, 0.3, 0.2, 0.1],
        k=1
    )[0]

    #Fiyat hesapla
    baz_fiyat=800 #baslangıç fiyat
    if marka in ['BMW','Mercedes']:
        baz_fiyat=2500
    elif marka in ['Toyota', 'Ford']:
        baz_fiyat = 1100
    elif model == 'Megane' or model == 'Egea': 
        baz_fiyat = 1000
    else: 
        baz_fiyat = 800

    #Yıl etkisi
    fiyat=baz_fiyat +(yil -2015) * 150

    # KM etkisi her 10.000 km için fiyat düşer
    fiyat -= (km / 10000) * 50

    #Hasar etkisi
    fiyat *= hasar_durumu[hasar]

    #Rastgele gürültü 
    noise=random.randint(-100,100)
    fiyat += noise

    if fiyat < 400: 
        fiyat = 400

    data.append([marka, model, km, hasar, yil, int(fiyat)])

df = pd.DataFrame(data, columns=['marka', 'model', 'km', 'hasar_durumu', 'model_yili', 'fiyat'])
df.to_csv('arac_kira_verisi.csv', index=False)
print("Veri seti oluşturuldu: arac_kira_verisi.csv")
print(df.head(10))