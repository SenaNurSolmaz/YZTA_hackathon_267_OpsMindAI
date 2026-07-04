<p align="center">
  <h1 align="center">🧠 OpsMind AI</h1>
  <p align="center"><strong>Yapay Zeka Destekli E-Ticaret Operasyon Yönetim Platformu</strong></p>
  <p align="center">
    Giyilebilir teknoloji ve VR/AR ürünleri için sipariş, kargo, stok, müşteri destek ve görev yönetimini tek bir panelde birleştiren akıllı operasyon platformu.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-15-black?logo=next.js" alt="Next.js 15" />
  <img src="https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Gemini_AI-3_Flash_Preview-4285F4?logo=google" alt="Gemini AI" />
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python" alt="Python" />
</p>

---

## 📋 İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [Özellikler](#-özellikler)
- [Mimari](#-mimari)
- [Teknoloji Yığını](#-teknoloji-yığını)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [API Referansı](#-api-referansı)
- [Veritabanı Şeması](#-veritabanı-şeması)
- [Proje Yapısı](#-proje-yapısı)
- [Entegrasyonlar](#-entegrasyonlar)
- [Test](#-test)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

---

## 🎯 Proje Hakkında

**OpsMind AI**, e-ticaret operasyonlarını yapay zeka ile optimize eden uçtan uca bir yönetim platformudur. Platform, sipariş takibinden kargo risk analizine, stok yönetiminden AI destekli müşteri hizmetlerine kadar tüm operasyonel süreçleri tek bir arayüzde birleştirir.

### Problem

E-ticaret operasyonlarında birçok farklı araç ve platform kullanılması, veri siloları oluşturur ve operasyonel verimliliği düşürür. Kargo gecikmeleri, stok tükenmesi ve müşteri şikayetleri reaktif olarak yönetilir.

### Çözüm

OpsMind AI, tüm operasyonel verileri merkezi bir dashboardda toplar ve **Gemini AI** ile proaktif öneriler sunarak:

- Kargo risklerini önceden tespit eder
- Stok tükenmelerini tahmin eder ve otomatik sipariş önerir
- Müşteri mesajlarına AI taslak yanıtlar oluşturur
- Operasyon raporlarını otomatik üretir
- Slack ve WhatsApp üzerinden anlık bildirimler gönderir

---

## ✨ Özellikler

### 📊 Genel Bakış Dashboard'u
- Günlük sipariş sayısı, ciro, riskli kargo ve AI çözülen talep KPI'ları
- Son siparişler tablosu (canlı akış)
- Fulfillment dağılımı (Kargoda / Hazırlanıyor / Gecikme / Teslim)
- AI tarafından oluşturulan operasyon özeti ve öncelik listesi
- Açık görevler ve son aktivite akışı

### 📬 AI Yardım Masası (Inbox)
- Müşteri konuşmalarının merkezi yönetimi
- **WhatsApp**, **Email** ve **Live Chat** kanal desteği
- AI tarafından otomatik oluşturulan yanıt taslakları
- Müşteri duygu analizi (Olumlu / Nötr / Olumsuz)
- Sipariş referansı ile otomatik bağlam eşleme
- Konuşma durumu takibi (AI Taslağı Hazır / Temsilci Bekliyor / Çözüldü)

### 🚚 Kargo Takibi
- Tüm kargoların gerçek zamanlı takibi
- Risk seviyesi analizi (Düşük / Orta / Yüksek)
- SLA saat takibi ve aşım uyarıları
- Kargo firması bazlı filtreleme (Yurtiçi, Aras, MNG, PTT, Sürat)
- CSV formatında kargo raporu dışa aktarma
- AI destekli kargo risk değerlendirmesi

### 📦 Stok Yönetimi (Envanter)
- SKU bazlı stok takibi
- Tükenme süresi hesaplama (gün bazında)
- Haftalık satış hızı (velocity) analizi
- Reorder point (yeniden sipariş noktası) yönetimi
- Tedarikçi teslim süresi takibi
- AI tarafından oluşturulan tedarik önerileri
- Tek tıkla sipariş oluşturma
- CSV formatında stok raporu dışa aktarma

### 📚 Bilgi Tabanı (Knowledge Base)
- Teknik destek, iade politikası ve kullanım kılavuzları
- Kategorize edilmiş bilgi makaleleri
- Yeni makale ekleme ve silme
- AI yanıt üretiminde referans olarak kullanılır

### ✅ Görev Yönetimi
- Operasyonel görevlerin oluşturulması ve takibi
- Sahip (owner) ve son tarih atama
- Durum yönetimi (Açık / Tamamlandı)
- Görev nedeni ve bağlam bilgisi

### ⚙️ Ayarlar
- **Kullanıcı yönetimi**: Ekleme, düzenleme, aktif/pasif yapma
- **Bildirim tercihleri**: Kanal bazlı bildirim ayarları (Slack, WhatsApp, E-posta)
- **Entegrasyon testi**: Slack, WhatsApp, Shopify, ChromaDB bağlantı kontrolü
- **AI rapor üretimi**: Operasyon özeti ve aksiyon önerileri
- Rol bazlı erişim (Admin, Operasyon, Destek, Satın Alma)

---

## 🏗 Mimari

```
┌──────────────────────────────────────────────────────┐
│                    KULLANICI                         │
│                  (Web Tarayıcı)                      │
└─────────────┬───────────────────────────┬────────────┘
              │                           │
              ▼                           ▼
┌─────────────────────┐     ┌──────────────────────────┐
│   Next.js Frontend  │───▶│    FastAPI Backend       │
│   (React 18 + TS)   │     │    (Python 3.11+)        │
│   Port: 3000        │     │    Port: 8000            │
│                     │     │                          │
│  • Dashboard        │     │  • REST API Endpoints    │
│  • AI Yardım Masası │     │  • Gemini AI Entegrasyon │
│  • Kargo Takibi     │     │  • Slack/WhatsApp        │
│  • Stok Yönetimi    │     │  • CSV Export            │
│  • Bilgi Tabanı     │     │  • DB İşlemleri          │
│  • Görevler         │     │                          │
│  • Ayarlar          │     └──────────┬───────────────┘
└─────────────────────┘                │
                                       ▼
                            ┌────────────────────────┐
                            │   PostgreSQL 16        │
                            │   (techops_db)         │
                            │                        │
                            │  9 Tablo:              │
                            │  users, orders,        │
                            │  shipments, inventory, │
                            │  conversations,        │
                            │  knowledge_base,       │
                            │  tasks, activity_log,  │
                            │  notification_prefs    │
                            └────────────────────────┘
```

> **Not:** Next.js, `/api/*` isteklerini `http://127.0.0.1:8000/api/*` adresine proxy olarak yönlendirir (bkz. `next.config.ts`).

---

## 🛠 Teknoloji Yığını

| Katman | Teknoloji | Versiyon |
|--------|-----------|----------|
| **Frontend** | Next.js (App Router) | 15.x |
| **UI** | React | 18.3 |
| **Dil (Frontend)** | TypeScript | 5.x |
| **Stil** | Vanilla CSS (Custom Design System) | — |
| **Font** | Inter (Google Fonts) | — |
| **Backend** | FastAPI | 0.111.0 |
| **ASGI Server** | Uvicorn | 0.30.1 |
| **Dil (Backend)** | Python | 3.11+ |
| **Veritabanı** | PostgreSQL | 16+ |
| **DB Driver** | asyncpg | 0.29.0 |
| **AI Model** | Google Gemini | 3 Flash Preview |
| **AI SDK** | google-generativeai | 0.7.1 |
| **Validasyon** | Pydantic | 2.7.4 |
| **Env Yönetimi** | python-dotenv | 1.0.1 |

---

## 🚀 Kurulum

### Ön Gereksinimler

- **Node.js** 18+ ve **npm**
- **Python** 3.11+
- **PostgreSQL** 16+
- **Google Gemini API Key** ([Google AI Studio](https://aistudio.google.com/app/apikey))

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/<kullanici>/opsmind-ai.git
cd opsmind-ai
```

### 2. Ortam Değişkenlerini Ayarlayın

```bash
cp .env.local.example .env.local
```

`.env.local` dosyasını düzenleyin:

```env
# Gemini AI (zorunlu)
GEMINI_API_KEY=buraya_gemini_api_key_yaz
GEMINI_MODEL=gemini-3-flash-preview

# Slack Webhook (opsiyonel — yoksa simülasyon modu çalışır)
SLACK_SUPPLY_WEBHOOK_URL=
SLACK_NOTIFY_WEBHOOK_URL=

# WhatsApp Business API (opsiyonel — yoksa simülasyon modu çalışır)
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_NOTIFY_NUMBER=

# Veritabanı (zorunlu)
DATABASE_URL=postgresql://postgres:SIFRENIZI_YAZIN@localhost:5432/techops_db

# NextAuth
NEXTAUTH_SECRET=en_az_32_karakter_rastgele_deger
NEXTAUTH_URL=http://localhost:3000
```

### 3. Veritabanını Oluşturun

pgAdmin veya `psql` ile yeni bir veritabanı oluşturun ve şema dosyasını çalıştırın:

```bash
# PostgreSQL'de veritabanı oluşturun
psql -U postgres -c "CREATE DATABASE techops_db;"

# Şema ve seed verilerini yükleyin
psql -U postgres -d techops_db -f db/schema_and_seed.sql
```

Bu komut 9 tablo oluşturur ve demo verileri (kullanıcılar, siparişler, kargolar, stok vb.) ekler.

### 4. Frontend Bağımlılıklarını Yükleyin

```bash
npm install
```

### 5. Backend (Python) Ortamını Kurun

```bash
# Sanal ortam oluşturun
python -m venv .venv

# Aktifleştirin
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r backend/requirements.txt
```

### 6. Uygulamayı Başlatın

İki ayrı terminal penceresi açın:

**Terminal 1 — Backend (FastAPI):**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Frontend (Next.js):**
```bash
npm run dev
```

Uygulama **http://localhost:3000** adresinde çalışacaktır.

---

## 💻 Kullanım

### Giriş Yapma

Uygulama demo kullanıcılarla çalışır. Aşağıdaki e-postalardan biriyle giriş yapın (şifre en az 4 karakter):

| Kullanıcı | E-posta | Rol | Departman |
|-----------|---------|-----|-----------|
| Ahmet Demir | `ahmet@opsmind.com` | Admin | Yönetim |
| Selin Kaya | `selin@opsmind.com` | Operasyon | Kargo & Lojistik |
| Barış Arslan | `baris@opsmind.com` | Destek | Müşteri Hizmetleri |

### Temel İş Akışları

1. **Dashboard'u İnceleyin** — Giriş yaptıktan sonra ana ekranda günün KPI'larını, riskli kargoları ve AI önerilerini görün.
2. **Kargo Risklerini Yönetin** — Kargo Takibi sayfasında yüksek riskli gönderileri filtreleyin ve durum güncellemesi yapın.
3. **AI Yardım Masası** — Müşteri mesajlarına AI'ın oluşturduğu taslak yanıtları inceleyin, düzenleyin ve gönderin.
4. **Stok Kontrolü** — Kritik stokları tespit edin, tek tıkla tedarik siparişi oluşturun.
5. **AI Rapor** — Ayarlar sayfasından operasyon raporunu AI ile oluşturun.

---

## 📡 API Referansı

Tüm API endpoint'leri `/api` prefix'i altında çalışır. Backend `http://127.0.0.1:8000` adresinde, Next.js proxy ile `http://localhost:3000/api/*` üzerinden erişilebilir.

### Genel

| Metod | Endpoint | Açıklama |
|-------|----------|----------|
| `GET` | `/api/health` | Sağlık kontrolü ve DB durumu |
| `GET` | `/api/dashboard` | Dashboard KPI, sipariş, görev ve aktivite verileri |

### Siparişler

| Metod | Endpoint | Açıklama |
|-------|----------|----------|
| `GET` | `/api/orders` | Tüm siparişleri listele |

### Kargo

| Metod | Endpoint | Açıklama |
|-------|----------|----------|
| `GET` | `/api/shipping` | Tüm kargoları listele |
| `GET` | `/api/shipping/export` | Kargo raporunu CSV olarak indir |
| `PUT` | `/api/shipping/{order_id}` | Kargo durumu/risk güncelle |

### Stok (Envanter)

| Metod | Endpoint | Açıklama |
|-------|----------|----------|
| `GET` | `/api/inventory` | Tüm stok kalemlerini listele |
| `GET` | `/api/inventory/export` | Stok raporunu CSV olarak indir |
| `PUT` | `/api/inventory/{sku}` | Stok bilgilerini güncelle |
| `POST` | `/api/inventory/order` | Tedarik siparişi oluştur |

### Konuşmalar (AI Yardım Masası)

| Metod | Endpoint | Açıklama |
|-------|----------|----------|
| `GET` | `/api/conversations` | Tüm konuşmaları listele |

### Görevler

| Metod | Endpoint | Açıklama |
|-------|----------|----------|
| `GET` | `/api/tasks` | Görevleri listele |
| `POST` | `/api/tasks` | Yeni görev oluştur |
| `PUT` | `/api/tasks/{id}` | Görev güncelle |
| `DELETE` | `/api/tasks/{id}` | Görev sil |

### Bilgi Tabanı

| Metod | Endpoint | Açıklama |
|-------|----------|----------|
| `GET` | `/api/knowledge` | Bilgi tabanı makalelerini listele |
| `POST` | `/api/knowledge` | Yeni makale ekle |
| `DELETE` | `/api/knowledge?id={id}` | Makale sil |

### Kullanıcılar

| Metod | Endpoint | Açıklama |
|-------|----------|----------|
| `GET` | `/api/users` | Kullanıcıları listele |
| `POST` | `/api/users` | Yeni kullanıcı ekle |
| `PUT` | `/api/users/{id}` | Kullanıcı güncelle |

### Bildirimler

| Metod | Endpoint | Açıklama |
|-------|----------|----------|
| `GET` | `/api/notifications` | Bildirim tercihlerini getir |
| `PUT` | `/api/notifications` | Bildirim tercihlerini güncelle |
| `POST` | `/api/notify` | Slack/WhatsApp bildirim gönder |
| `POST` | `/api/supply-webhook` | Tedarik webhook simülasyonu |

### AI Endpoint'leri

| Metod | Endpoint | Açıklama |
|-------|----------|----------|
| `POST` | `/api/agent` | Genel amaçlı AI yanıt üretimi |
| `POST` | `/api/ai-draft` | Müşteri mesajına AI taslak yanıt |
| `POST` | `/api/report` | AI operasyon raporu üretimi |
| `POST` | `/api/integration-test` | Entegrasyon bağlantı testi |

---

## 🗄 Veritabanı Şeması

```mermaid
erDiagram
    users {
        text id PK
        text name
        text email UK
        text role
        text department
        boolean active
        timestamptz created_at
    }

    orders {
        text id PK
        text name
        text customer
        text city
        numeric total_try
        text payment_status
        text fulfillment_status
        int item_count
        text channel
        text product
        timestamptz created_at
    }

    shipments {
        serial id PK
        text order_id FK
        text customer
        text provider
        text tracking_no
        text destination
        text status
        text risk
        int sla_hours_left
        date estimated_delivery
        text product
    }

    inventory {
        text sku PK
        text product
        text category
        int stock
        int reorder_point
        int weekly_velocity
        int depletion_days
        text recommendation
        int supplier_lead_days
        numeric unit_price
    }

    conversations {
        text id PK
        text customer
        text channel
        text topic
        text status
        text sentiment
        text order_ref
        text ai_draft
    }

    knowledge_base {
        text id PK
        text title
        text content
        text category
        text added_by
    }

    tasks {
        text id PK
        text title
        text owner
        text due
        text reason
        text status
    }

    activity_log {
        serial id PK
        timestamptz event_time
        text text
    }

    notification_preferences {
        text key PK
        text label
        text target
        boolean enabled
    }

    orders ||--o{ shipments : "has"
```

---

## 📁 Proje Yapısı

```
opsmind-ai/
├── app/                          # Next.js App Router (Frontend)
│   ├── globals.css               # Tasarım sistemi ve tüm stiller
│   ├── layout.tsx                # Root layout (AuthProvider)
│   ├── page.tsx                  # Dashboard ana sayfa
│   ├── login/page.tsx            # Giriş ekranı
│   ├── inbox/page.tsx            # AI Yardım Masası
│   ├── shipping/page.tsx         # Kargo Takibi
│   ├── inventory/page.tsx        # Stok Yönetimi
│   ├── knowledge-base/page.tsx   # Bilgi Tabanı
│   ├── tasks/page.tsx            # Görev Yönetimi
│   └── settings/page.tsx         # Ayarlar
│
├── components/                   # Paylaşılan React bileşenleri
│   ├── navigation.tsx            # Sidebar navigasyon
│   └── page-shell.tsx            # Sayfa düzeni şablonu
│
├── lib/                          # Yardımcı kütüphaneler
│   ├── auth.tsx                  # Kimlik doğrulama (Context API)
│   ├── api-error.ts              # API hata mesajı çözümleyici
│   └── mock-data.ts              # TypeScript tip tanımları
│
├── backend/                      # FastAPI Backend (Python)
│   ├── main.py                   # FastAPI uygulama giriş noktası
│   ├── requirements.txt          # Python bağımlılıkları
│   └── app/
│       ├── __init__.py
│       ├── db.py                 # PostgreSQL bağlantı ve sorgu yöneticisi
│       └── api/                  # API endpoint modülleri
│           ├── dashboard.py      # Dashboard KPI ve verileri
│           ├── agent.py          # Gemini AI genel yanıt
│           ├── ai_draft.py       # Müşteri yanıt taslağı
│           ├── report.py         # AI operasyon raporu
│           ├── shipping.py       # Kargo CRUD + CSV export
│           ├── inventory.py      # Stok CRUD + sipariş + CSV export
│           ├── orders.py         # Sipariş listeleme
│           ├── conversations.py  # Konuşma yönetimi
│           ├── tasks.py          # Görev CRUD
│           ├── knowledge.py      # Bilgi tabanı CRUD
│           ├── users.py          # Kullanıcı CRUD
│           ├── notifications.py  # Bildirim tercihleri
│           ├── notify.py         # Slack/WhatsApp bildirim
│           ├── supply_webhook.py # Tedarik webhook
│           └── activity_log.py   # Aktivite logu
│
├── db/
│   └── schema_and_seed.sql       # PostgreSQL şema ve demo veriler
│
├── scripts/
│   └── backend_smoke.py          # Backend smoke test
│
├── public/
│   └── favicon.svg               # Uygulama ikonu
│
├── .env.local.example            # Ortam değişkenleri şablonu
├── .gitignore
├── next.config.ts                # Next.js yapılandırması (API proxy)
├── tsconfig.json                 # TypeScript yapılandırması
├── package.json                  # Node.js bağımlılıkları
└── package-lock.json
```

---

## 🔗 Entegrasyonlar

| Entegrasyon | Durum | Açıklama |
|-------------|-------|----------|
| **Google Gemini AI** | ✅ Aktif | Müşteri yanıt taslağı, operasyon raporu ve genel AI asistan |
| **Slack** | 🔄 Opsiyonel | Webhook ile kargo uyarıları ve operasyon bildirimleri |
| **WhatsApp Business** | 🔄 Opsiyonel | Graph API ile müşteri bildirimleri |
| **Shopify** | 🔮 Simülasyon | Webhook simülasyonu (gelecek entegrasyon) |
| **ChromaDB** | 🔮 Simülasyon | Vektör veritabanı (gelecek entegrasyon) |

> **Simülasyon Modu:** Slack ve WhatsApp kimlik bilgileri tanımlı değilse, sistem otomatik olarak simülasyon modunda çalışır. Bildirimlerin çıktısı sunucu loglarında görünür.

---

## 🧪 Test

### Backend Smoke Test

Tüm API endpoint'lerini doğrulayan bir smoke test scripti mevcuttur:

```bash
# Sanal ortam aktifken
npm run test:backend

# veya doğrudan
.venv/Scripts/python.exe scripts/backend_smoke.py
```

Bu test şunları doğrular:
- Health check endpoint'i
- Dashboard verilerinin getirilmesi
- Görev CRUD işlemleri (oluştur → güncelle → sil)
- Stok güncelleme ve sipariş oluşturma
- Kargo listeleme
- Kullanıcı CRUD işlemleri
- Bildirim tercihleri CRUD
- Bilgi tabanı CRUD
- Webhook ve bildirim simülasyonları
- AI draft endpoint (API key yoksa hata kontrolü)

### TypeScript Tip Kontrolü

```bash
npm run typecheck
```

---

## 🤝 Katkıda Bulunma

1. Bu depoyu fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request açın

---

## 📄 Lisans

Bu proje hackathon kapsamında geliştirilmiştir.

---

<p align="center">
  <strong>OpsMind AI</strong> ile operasyonlarınızı akıllı hale getirin. 🚀
</p>

---

## 👥 Ekip ve Rol Dağılımı

[cite_start]Bu proje, **Yapay Zeka ve Teknoloji Akademisi (YZTA 5.0)** kapsamında düzenlenen Hackathon & Datathon etkinliğinde [cite: 1, 3][cite_start], 5 kişilik bir yapay zeka bursiyeri ekibi tarafından 5 günlük yoğun bir süreçte uçtan uca geliştirilmiştir[cite: 3, 5].

* [cite_start]**Sena Nur Solmaz (Product / Delivery Lead):** Ürün vizyonunun ve MVP (Minimum Uygulanabilir Ürün) kapsamının belirlenmesi[cite: 104]; [cite_start]KOBİ'lerin manuel operasyonel problemlerinin analizi [cite: 4, 320][cite_start]; n8n iş akışlarının mantıksal kurgusu ve backend entegrasyon stratejisi[cite: 90]; [cite_start]1 dakikalık jüri sunumunun hikayeleştirilmesi ve video scriptinin hazırlanması[cite: 82, 91].
* [cite_start]**Beste Avcı (AI & Frontend Developer):** Next.js 15 tabanlı proaktif yönetim dashboard arayüzünün tasarımı [cite: 64, 196] [cite_start]ve yapay zeka destekli müşteri yardım masası (Inbox) görsel bileşenlerinin geliştirilmesi[cite: 196].
* [cite_start]**Koray Öztürk (AI & Backend Developer):** FastAPI & Python tabanlı backend mimarisinin kurulması [cite: 64, 128][cite_start], PostgreSQL ilişkisel veritabanı şemasının tasarlanması ve Gemini AI ajan entegrasyonlarının kodlanması[cite: 121, 197].
* [cite_start]**Burak Koçaş (AI & Support Developer):** Bilgi Tabanı (Knowledge Base) sistem mimarisinin kurgulanması [cite: 101][cite_start], RAG (Retrieval-Augmented Generation) yaklaşımı için AI prompt ve grounding optimizasyonlarının yapılması[cite: 89, 119].
* [cite_start]**Aslı Tiryaki (Support Developer):** Ayarlar, görev yönetimi ve kullanıcı rol bazlı erişim mekanizmalarının entegrasyonu [cite: 101][cite_start]; kargo, stok ve veri analitiği CSV export fonksiyonlarının test süreçleri[cite: 101].

---

## 🎯 Ürün Yönetimi ve Proaktif İş Akışları Tasarımı (Product Lead Notu)

[cite_start]Yazılım dünyasındaki geliştirme commit'leri teknik roller tarafından atılmış olsa da [cite: 189][cite_start], platformda can bulan tüm akıllı operasyonel senaryoların ve iş kurallarının arkasındaki ürün mimarisi tarafımdan kurgulanmıştır[cite: 190]. [cite_start]Projede jüriden tam puan alan ve mülakatlarda değer yaratan 3 kritik proaktif senaryo tasarımı şudur[cite: 93, 210]:

### 1. Reaktif Değil, Proaktif Kargo Risk Yönetimi
[cite_start]Geleneksel e-ticaret yazılımlarında kargo gecikmeleri ancak müşteri şikayet ettiğinde fark edilir[cite: 318]. [cite_start]Kurguladığım mimaride, kargo firmasının API'sinden (simüle) gelen gecikme sinyalleri sistem tarafından otomatik yakalanır[cite: 328]. [cite_start]Müşteri daha durumun farkına varmadan AI tarafından bir bilgilendirme mesajı hazırlanır ve eş zamanlı olarak operasyon yöneticisinin paneline yüksek riskli görev olarak atanır[cite: 329].

### 2. Akıllı İletişim & Sıfır Halüsinasyon (Grounding)
[cite_start]Müşterilerin "128 numaralı siparişim nerede?" gibi sorularına büyük dil modellerinin ezbere veya uydurma (hallucination) cevaplar vermesini engellemek adına [cite: 89, 323][cite_start], yapay zekayı doğrudan PostgreSQL veritabanımızdaki gerçek sipariş ve SLA verileriyle besleyecek (RAG) mantıksal köprüyü kurdum[cite: 89, 119]. [cite_start]AI, veritabanından aldığı kargo durumunu WhatsApp/Email kanallarına insan müdahalesi olmadan otomatik olarak yanıt taslağı hazırlar[cite: 324].

### 3. Kritik Eşikli Otomatik Tedarik Önerisi
[cite_start]Bir tarım veya e-ticaret işletmesinde stok bittikten sonra aksiyon almak ciro kaybına yol açar[cite: 317, 331]. [cite_start]Sistemde envanter seviyeleri otomatik izlenirken, belirlenen kritik eşiklerin (Örn: Organik Domates < 50kg) altına düşüldüğü an sistem proaktif olarak devreye girer[cite: 330, 331]. [cite_start]Geçmiş satış hızını (velocity) analiz ederek ne kadar sipariş verilmesi gerektiğini hesaplar ve satın alma sorumlusuna Slack/WhatsApp üzerinden taslak bir tedarik siparişi iletir[cite: 331].****
