# flaskornek projesi kullanımı
*Projedeki models klasöründe veritabanında oluşacak tablolarımız mevcut. Bir tabloyu tüm özellikleri ile burada tanımlıyoruz.

*Controllers klasörümüz ise aslında tüm metodlarımızı tablolara ve tablo ilişkilerine göre tanımladığımız kısımlar.

*config dosyamız şu anlık temsili olarak var ama gerçek zamanlı çalışacağımız zaman veritabanı tabloları oluşturulurken, veri tabanı bağlantısını sağlayan ve db=SQLAchemy tanımlamasının yapıldığı yer.

*db_init dosyamız ise config üzerinden bağlanılan veritabanımızda models olarak belirttiğimiz tabloların oluşturulmasını sağlıyor.(bu şu anda projenin bir veritabanı olmadığı için çalışmayacak.)

*app.py dosyamız flaskapi projemizin ana çalışma dosyası bu dosya terminal üzerinden python app.py komutu yazılarak çalıştırılabilir. Bu dosya çalıştıktan sonra bize verilen terminal çıktısındaki URL projenin çalıştığı yer oluyor. Bunu bir tarayıcı sekmesinde deneyebilirsin. Asıl deneme işlemlerini beraber Postman üzerinde yapacağız.

*requirements dosyamız ise bir kolaylık dosyası, pip install -r requirements.txt komutunu Pycharm terminalinde çalıştırarak projenin çalışması için gerekli tüm bağımlılıkları projeye yükleyebilirsin.

*Controller dosyaları içindeki metodları incelerken kullanılan parametreleri models klasöründeki tablo özellikleriyle kıyaslamak. Onun haricinde ise metodlarımızın get ve post özelliklerine dikkat etmek önemli.
