# OpsMind AI - Yeni Bilgisayar Kurulum Rehberi

Bu rehberi arkadaşınızla paylaşın. Adımları sırayla yapın.

---

## 1. PostgreSQL Kur

1. [postgresql.org/download/windows](https://www.postgresql.org/download/windows/) adresine gir
2. **PostgreSQL 18** için "Download the installer" butonuna tıkla
3. Kurulumu çalıştır:
   - **Password:** Aklında kalacak bir şifre belirle (örnek: `1234`)
   - **Port:** `5432` (varsayılan, değiştirme)
   - Diğer seçenekler varsayılan kalabilir
4. Kurulum bitince **Stack Builder** penceresini kapat (Next > Cancel)

---

## 2. Veritabanını Oluştur

Windows başlat menüsünden **SQL Shell (psql)** aç. Şu soruları soracak:

```
Server [localhost]: ENTER
Database [postgres]: ENTER
Port [5432]: ENTER
Username [postgres]: ENTER
Password for user postgres: <belirledigin sifreyi yaz>
```

Giris yapinca asagidaki komutu yaz ve Enter'a bas:

```sql
CREATE DATABASE techops_db;
```

`CREATE DATABASE` yazisi gorursen basarili. Simdi psql'i kapat:
```
\q
```

---

## 3. Tabloları ve Verileri Yukle

Proje klasorunde bir **PowerShell** penceresi ac ve su komutu calistir:

> **Sifreyi kendininkiyle degistir**

```powershell
$env:PGPASSWORD='SIFRENIZI_YAZIN'; & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d techops_db -f "db\schema_and_seed.sql"
```

Ekranda bir suru `CREATE TABLE`, `INSERT` ve en sonda su tablo gorurseniz basarili:

```
         tablo          | count
------------------------+-------
 users                  |     4
 orders                 |     5
 shipments              |     5
 inventory              |     5
 conversations          |     4
 knowledge_base         |     3
 tasks                  |     3
 activity_log           |     4
 notification_preferences|     5
```

---

## 4. Env Dosyasini Hazirla

Proje klasorundeki `.env.local.example` dosyasini **kopyala** ve `.env.local` olarak kaydet.

Sonra icini du:

```
DATABASE_URL=postgresql://postgres:SIFRENIZI_YAZIN@localhost:5432/techops_db
GEMINI_API_KEY=buraya_gemini_api_key_yaz
```

Diger alanlari (Slack, WhatsApp) doldurmak zorunda degilsin, bos birakabilirsin — simulasyon modunda calisir.

> **Gemini API Key nereden alinir?**
> [aistudio.google.com](https://aistudio.google.com) > "Get API Key" > "Create API Key"

---

## 5. Python Bagimlilikları Kur

Proje klasorunde PowerShell ac:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 6. Node Bagimlilikları Kur

Ana proje klasorunde PowerShell ac:

```powershell
npm install
```

---

## 7. Projeyi Calistir

**2 ayrı terminal** aç:

**Terminal 1 - Backend:**
```powershell
cd backend
.venv\Scripts\Activate.ps1
python -m uvicorn main:app --port 8000
```

**Terminal 2 - Frontend:**
```powershell
npm run dev
```

Sonra tarayicida [http://localhost:3000](http://localhost:3000) adresini ac.

---

## Sorun Giderme

| Hata | Cozum |
|------|-------|
| `psql is not recognized` | PowerShell'i yeniden baslat veya PATH'e `C:\Program Files\PostgreSQL\18\bin` ekle |
| `Connection refused` port 5432 | PostgreSQL servisi calismıyor — Baslat > Hizmetler > PostgreSQL > Baslat |
| `GEMINI_API_KEY tanimli degil` | `.env.local` dosyasini kontrol et, backend klasorunde mi? |
| `Module not found` Python | `.venv\Scripts\Activate.ps1` ile venv'i aktive et, sonra `pip install -r requirements.txt` tekrar calistir |
| Frontend boş sayfa | Backend'in port 8000'de calistigini kontrol et |
