# arac-kiralama-projesi

**Bu projeyi Bilgisayar Programlama 2 dersimiz kapsamında 3 kişilik bir ekip ile geliştirdik. Temel amacımız, derste öğrendiğimiz Python kodlama tekniklerini ve Nesne Yönelimli Programlama (OOP) mantığını gerçek bir uygulama üzerinde birleştirmekti.
Ortaya çıkardığımız bu sistem sayesinde araçların ve müşterilerin kaydı tutulabiliyor, kiralama işlemleri karışıklık olmadan yönetilebiliyor. Kısacası hedefimiz, öğrendiklerimizi kullanarak çalışan, akıllı ve işe yarar bir sistem yapmaktı.**

________________________________________

Proje, katmanlı bir yapıda tasarlanmıştır:

•	ui/: Kullanıcı arayüzü kodları

•	manager/: Veritabanı yönetimi

•	models/: Veri yapıları 

•	ai/: Yapay zeka algoritması

•	data/: Veritabanı dosyaları

________________________________________

**Kullanılan Teknolojiler ve Kütüphaneler Proje geliştirme sürecinde aşağıdaki Python kütüphanelerinden yararlanılmıştır:**

•	*CustomTkinter: Modern GUI tasarımı, Dark/Light mode desteği ve ölçeklenebilir widget'lar için kullanılmıştır.*

•	*Scikit-Learn: RandomForestRegressor ile fiyat tahmini yapmak, LabelEncoder ile veriyi işlemek için kullanılmıştır.*

•	*Pandas & NumPy: Veri setinin analizi ve matris işlemleri için kullanılmıştır.*

•	*Matplotlib: Yönetici panelindeki finansal verilerin (Pasta ve Sütun grafikleri) görselleştirilmesi için kullanılmıştır.*

•	*Joblib: Eğitilen yapay zeka modelinin .pkl formatında kaydedilmesi ve yüklenmesi için kullanılmıştır.*

•	*Tkcalendar: Tarih seçimi işlemleri için takvim bileşeni olarak kullanılmıştır.*

•	*OS, JSON, Re, Datetime: Dosya yönetimi, veri saklama, regex ile validasyon ve tarih hesaplamaları için kullanılmıştır.*

________________________________________

**Yapay Zeka Tabanlı Fiyat Tahmin Modülü**

Bu modül, araçların teknik özelliklerini analizerek yöneticilere ideal kiralama fiyatını önerir. Geliştirme süreci üç temel aşamadan oluşur:

Sentetik Veri Üretimi (yapay_veri.py): Numpy ve Pandas kullanılarak, gerçek piyasa koşullarını (marka bilinirliği, model yılı, hasar durumu vb.) simüle eden 400 satırlık ağırlıklı ve gürültü eklenmiş veri seti oluşturulmuştur.

Model Eğitimi (price_model.py): Veriler, Label Encoding ve Standard Scaling teknikleriyle işlenerek makine öğrenmesine hazır hale getirilmiştir. Tahmin algoritması olarak Random Forest Regressor kullanılmış; eğitilen model ve dönüştürücüler .pkl formatında kaydedilmiştir.

Tahmin Mekanizması (price_estimate.py): Kullanıcının arayüzden girdiği veriler, kayıtlı model ve scaler'lar kullanılarak işlenir ve sistem anlık olarak araç için fiyat tahmini üretir.

________________________________________

**SONUÇ VE DEĞERLENDİRME**

Bu proje çalışması sonucunda, ders kapsamında öğrenmiş olduğumuz bilgiler kullanılarak kapsamlı bir "Araç Kiralama Sistemi" geliştirilmiştir. Proje süresince:

1.	Teknik Yetkinlik: Python, OOP, JSON yönetimi ve CustomTkinter ile GUI tasarımı konularında yetkinlik kazanılmıştır.

2.	Yapay Zeka Entegrasyonu: Teorik Yapay Zeka algoritmalarının, gerçek bir yazılım projesine entegrasyonu gerçekleştirilmiştir.

3.	Veri Yönetimi: İlişkisel olmayan bir veri yapısında (JSON) veri bütünlüğünün nasıl sağlanacağı kodlanarak deneyimlenmiştir.

Sistem testleri sonucunda, uygulamanın stabil çalıştığı, kullanıcı hatalarına karşı dirençli olduğu ve fiyat tahmin modülünün tutarlı sonuçlar ürettiği gözlemlenmiştir.



