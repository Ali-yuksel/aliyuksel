import psycopg
from fastapi import FastAPI
import uvicorn
app=FastAPI()

# 1. PostgreSQL Veritabanına Bağlantı Açma
# (Kendi kullanıcı adı, şifre ve veritabanı adınızı yazın)

connection="dbname=test_db user=postgres password=12345678! host=localhost port=5432"

try:
    #veritabani bağlantısını başlatır ..
    with psycopg.connect(connection)as conn:
        # cursor imleç sql sorgularını çaliştirmamizi sağlayan araç 
        with conn.cursor() as cur:
            print("1. tablo oluşturuluyor...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS urunler (\
                id SERIAL PRIMARY KEY,  \
                urun_id VARCHAR(100) NOT NULL, \
                fiyat DECİMAL (10,1) NOT NULL \
                );
            """)
            # SQL Injection riskini önlemek için parametreli (%s) güvenli sorgu kullanıyoruz
            print("2. tabloya veri ekliyor...")
            sql_ekle=" INSERT INTO urunler(urun_id,fiyat)VALUES (%s,%s);"
            # Eklemek istediğimiz gerçek veriler (Örn: API'den gelen veriler)
            yeni_urun=("oyuncu klavyesi",1850,50)
            cur.execute(sql_ekle,yeni_urun)
            print("3. eklenen veriler kodla geri okunuyor..")
            cur.execute("SELECT * FROM urunler;")
            # Gelen tüm satırları Python listesi olarak alıyoruz
            tum_urunler=cur.fetchall()
            for urun in tum_urunler:
                print(f"veritabanindan gelen -> ID {urun[0]},isim: {urun[1]}fiyat:{urun[2]}")
                # 'with' bloğu bittiğinde 'conn.commit()' otomatik çalışır ve veriler kalıcı olarak kaydedilir.
                print("\n İşlem başarıyla tamamlandı, bağlantı güvenli şekilde kapatıldı.")
except Exception as e:
    print(f"veritabani işlemi sırasinda bir hata oluştur : {e}")

# 1. Endpoint: Ana Sayfa (Test amaçlı)
@app.get("/")
def desktop():
    return {"mesaj":"github codespace API canlıda"}


# 2. Endpoint: Tüm Ürünleri PostgreSQL'den Çeken API (GET)
@app.get("/urunler")
def urunler_get():
    with psycopg.connect(connection) as conn:
        with conn.cursor()as cur:
            cur.execute("SELECT * FROM GİTHUB_URNLERİ;")
            satirlar=cur.fetchall()
            # Veritabanı sonuçlarını JSON formatına çeviriyoruz
            liste=[]
            for satir in satirlar:
                liste.append({"id":satir[0],"urun_id":satir[1],"fiyat":satir[2]})
                return liste
            
            # 3. Endpoint: Veritabanına Yeni Ürün Ekleyen API (POST)
@app.post("/urun-ekle")
def post_get(urun_id:str,fiyat:float):
    with psycopg.connect(connection) as con:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO github_urunleri (urun_id,fiyat) VALUES (%S,%S) RETURNING,id;",
                (urun_id,fiyat)
            )
            yeni_id=cur.fetchall()[0]
            return {"mesaj":"ürün eklendi","eklenen_id":yeni_id}
def api():
    uvicorn.run("database_veritabani:app",host="0.0.0.0",port=8000,reload=True)
if(__name__=="__main__"):
    api()
