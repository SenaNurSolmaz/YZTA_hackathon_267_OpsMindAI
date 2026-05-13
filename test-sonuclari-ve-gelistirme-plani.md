# OpsMind AI Test Sonuçları ve Geliştirme Planı

Tarih: 2026-05-13

Bu doküman, uygulama geliştirmeye başlamadan önce yapılan uçtan uca testlerden çıkan gerçek bulguları ve bunlara göre izlenecek geliştirme planını içerir. Amaç, sohbet içinde kaybolmayacak kalıcı bir referans oluşturmak ve sonraki geliştirme adımlarını bu dosya üzerinden takip etmektir.

## Uygulama Durumu

2026-05-13 geliştirme turunda uygulananlar:

- P0 auth hydration/deep-link hatası düzeltildi.
- Bozuk `localStorage` oturum verisi güvenli şekilde temizlenir hale getirildi.
- Oturum varken `/inventory`, `/shipping`, `/settings` gibi direkt route açılışları doğrulandı.
- `/knowledge` route'u `/knowledge-base` sayfasına redirect edecek şekilde eklendi.
- API hata mesajları için ortak `apiErrorMessage` helper'ı eklendi.
- Gemini hata mesajı artık backend `detail` alanını okuyacak şekilde düzeltildi.
- Bilgi tabanı, stok, kargo ve ayarlar tarafında kritik API hata mesajları daha anlaşılır hale getirildi.
- Entegrasyon testlerinde son test bilgisi statik metin yerine state üzerinden güncellenir hale getirildi.
- Aktif admin kullanıcısının kendi oturumunu deaktive etmesi engellendi.
- Görev ve kullanıcı modal inputları daha erişilebilir/test edilebilir hale getirildi.
- SVG favicon eklendi ve metadata içine bağlandı.
- Backend smoke testi `scripts/backend_smoke.py` olarak repo içine alındı.
- `package.json` içine `typecheck` ve `test:backend` scriptleri eklendi.

Bu turda doğrulananlar:

- `npm run typecheck` başarılı.
- `npm run build` başarılı.
- `npm run test:backend` başarılı.
- `npm audit --audit-level=moderate` başarılı, 0 vulnerability.
- Production auth regression smoke başarılı:
  - `/inventory` direkt açıldı.
  - `/shipping` direkt açıldı.
  - `/settings` direkt açıldı.
  - `/knowledge` redirect'i çalıştı.
  - Bozuk `localStorage` temizlenip login'e yönlendi.

Kalanlar:

- Playwright UI smoke testinin repo bağımlılığı olarak kalıcı hale getirilmesi.
- Backend kapalıyken console'da görülen proxy 500 logları için isteğe bağlı demo veri göstergesi.

Audit notu:

- `next` altındaki `postcss` bağımlılığı `overrides` ile `8.5.14` sürümüne sabitlendi.
- Bu işlem `next` sürümünü düşürmeden audit uyarısını kapattı.
- `npm run typecheck`, `npm run build` ve `npm run test:backend` tekrar başarılı çalıştı.

## Kapsam

Bu test turunda Docker kurulmadan, mevcut in-memory FastAPI backend ve Next.js frontend birlikte çalıştırıldı. Üretim build'i, TypeScript kontrolü, backend endpoint smoke testleri, production mod UI akışları ve backend kapalı fallback davranışları kontrol edildi.

Bu turda kapsam dışı bırakılanlar:

- PostgreSQL bağlantısı ve kalıcı veritabanı geçişi
- Docker Compose ortamı
- Gerçek NextAuth / production auth mimarisi
- Gerçek WhatsApp production gönderimleri
- Gerçek Slack webhook gönderimleri
- Gemini kota/ücretli kullanım doğrulaması

## Çalıştırılan Doğrulamalar

### Frontend Build ve TypeScript

- `npm run build`
  - Sonuç: Başarılı.
  - Next.js production build alındı.
  - Static page generation tamamlandı.
  - `/inventory` ve `/shipping` prerender/runtime crash üretmedi.

- `npx tsc --noEmit`
  - Sonuç: Başarılı.
  - TypeScript seviyesinde hata bulunmadı.

### Backend Smoke Test

FastAPI `TestClient` ile temel endpointler test edildi.

Geçen kontroller:

- `GET /api/health`
- `GET /api/dashboard`
- `GET /api/tasks`
- `POST /api/tasks`
- `PUT /api/tasks/{task_id}`
- `DELETE /api/tasks/{task_id}`
- `GET /api/inventory`
- `PUT /api/inventory/{sku}`
- `POST /api/inventory/order`
- `GET /api/shipping`
- `GET /api/users`
- `POST /api/users`
- `PUT /api/users/{user_id}`
- `GET /api/notifications`
- `PUT /api/notifications`
- `GET /api/knowledge`
- `POST /api/knowledge`
- `DELETE /api/knowledge`
- `POST /api/supply-webhook`
- `POST /api/notify`
- `POST /api/integration-test`
- `POST /api/ai-draft` Gemini key yokken beklenen Türkçe hata ile döndü.

Sonuç: 22/22 başarılı.

### Production UI Akış Testi

Production build sonrası Next.js `next start` ile çalıştırıldı ve Playwright ile kullanıcı akışları gezildi.

Geçen ana akışlar:

- Login doğrulaması ve başarılı giriş
- Dashboard içeriklerinin görünmesi
- Sidebar daraltma/genişletme
- Inbox konuşma seçimi
- Inbox'tan bilgi tabanına kayıt ekleme
- Inbox temsilciye devretme
- Inbox yanıt gönderme
- Gemini key yokken kullanıcıya hata gösterme
- Kargo risk filtreleri
- Kargo satır seçimi
- Kargo proaktif bildirim simülasyonu
- Kargo CSV raporu indirme
- Stok satır seçimi
- Stok düzenleme modalı
- Stok tedarik siparişi verme
- Stok tedarik taslağı simülasyonu
- Kritik SKU CSV indirme
- Bilgi tabanı arama
- Bilgi tabanı kayıt ekleme
- Bilgi tabanı kayıt silme
- Görev ekleme
- Görev tamamlama
- Görev silme
- Ayarlar kullanıcı ekleme
- Kullanıcı rol güncelleme
- Entegrasyon test butonu
- Entegrasyon ayar modalı
- Bildirim tercihlerini kaydetme
- Logout sonrası korumalı route'un login'e yönlenmesi
- Mobil viewport smoke testi

Sonuç: 10/11 başarılı.

Başarısız olan test:

- LocalStorage içinde kullanıcı varken direkt `/inventory` açıldığında uygulama `/login` sayfasına yönlendi.

Bu gerçek bir auth/deep-link hatasıdır.

### Backend Kapalı Fallback Testi

Backend kapalıyken production frontend çalıştırıldı. Kritik sayfalar gezildi.

Geçen sayfalar:

- Dashboard
- Kargo Takibi
- Stok Durumu
- Görev Merkezi
- Ayarlar
- Bilgi Tabanı

Sonuç: Sayfalar crash olmadan açıldı.

Not: Backend kapalı olduğu için browser console'da `/api/*` proxy kaynaklı 500 logları görüldü. Kullanıcı ekranı kırılmadı.

### Güvenlik / Audit

`npm audit --audit-level=moderate` sonucu:

- 2 moderate uyarı var.
- Kaynak: `next` bağımlılığı üzerinden `postcss`.
- `npm audit fix --force` önerisi kırıcı şekilde eski `next@9.3.3` kurmayı öneriyor.

Karar:

- `npm audit fix --force` uygulanmayacak.
- Güvenli upgrade/override stratejisi ayrıca değerlendirilecek.

## Net Hatalar

### P0 - Auth Deep-Link / Reload Hatası

Durum:

- Kullanıcı localStorage içinde kayıtlı olsa bile direkt `/inventory` gibi korumalı bir route açıldığında uygulama `/login`e düşüyor.

Muhtemel sebep:

- `AuthProvider` ilk render anında `user=null` görüyor.
- localStorage okuma işlemi tamamlanmadan redirect effect'i çalışıyor.
- Bu yüzden geçerli oturum olmasına rağmen kullanıcı login sayfasına yönleniyor.

Etkisi:

- Kullanıcı sayfayı yenileyince bulunduğu sayfayı kaybedebilir.
- Direkt link paylaşımı veya bookmark ile açılış bozulur.
- Demo deneyimi açısından kritik bir hata.

Çözüm planı:

- `AuthProvider` içine `authReady` veya `hydrated` state'i eklenecek.
- localStorage okuma tamamlanmadan redirect yapılmayacak.
- localStorage içindeki bozuk JSON güvenli şekilde temizlenecek.
- Kullanıcı `/login` sayfasındayken zaten oturum varsa `/` sayfasına yönlendirilecek.

Kabul kriterleri:

- Login olmuş kullanıcı `/inventory` direkt açınca Stok Durumu sayfasında kalmalı.
- Login olmuş kullanıcı `/shipping` direkt açınca Kargo Takibi sayfasında kalmalı.
- Login olmuş kullanıcı `/settings` direkt açınca Ayarlar sayfasında kalmalı.
- Oturum yokken korumalı route açılırsa `/login`e yönlenmeli.
- Bozuk localStorage değeri uygulamayı crash etmemeli.

### P1 - Gemini Hata Mesajı Frontend'de Eksik Okunuyor

Durum:

- Backend Gemini hatalarında `detail` alanı dönüyor.
- Bazı frontend akışlarında hata `data.error ?? "unknown"` şeklinde okunuyor.
- Bu, kullanıcıya "unknown" gibi zayıf hata metni gösterme riski oluşturuyor.

Etkisi:

- Gemini API key yokken veya kota doluyken kullanıcı neden hata aldığını net göremeyebilir.
- Backend'de standardize edilen Türkçe hata mesajı frontend'e tam yansımayabilir.

Çözüm planı:

- Frontend tarafında ortak hata okuma helper'ı eklenecek.
- Okuma sırası: `detail`, `error`, `message`, fallback genel mesaj.
- Inbox Gemini akışı bu helper'ı kullanacak.
- Entegrasyon, notify ve supply akışlarında da aynı yaklaşım değerlendirilecek.

Kabul kriterleri:

- Gemini API key yokken kullanıcı "Gemini API anahtarı tanımlı değil..." benzeri Türkçe mesajı görmeli.
- 429/kota durumunda kullanıcı kota mesajını görmeli.
- Frontend'de "unknown" mesajı kalmamalı.

### P1 - Route İsimlendirme Tutarsızlığı

Durum:

- UI sayfası `/knowledge-base`.
- API endpoint'i `/api/knowledge`.
- Önceki planlarda ve konuşmalarda bazen `/knowledge` gibi ifade edilebiliyor.

Etkisi:

- Geliştirme sırasında yanlış route referansı kullanılabilir.
- Test planı ve dokümanlarda karışıklık yaratır.

Çözüm seçenekleri:

- Seçenek A: UI route'u `/knowledge-base` olarak bırakıp dokümantasyonda netleştirmek.
- Seçenek B: `/knowledge` route'u için redirect eklemek.

Öneri:

- Demo aşamasında mevcut `/knowledge-base` korunabilir.
- Kullanıcı dostu kısa route istenirse sonraki turda `/knowledge` redirect'i eklenebilir.

Kabul kriterleri:

- Navigasyon ve dokümanlar aynı route adını kullanmalı.
- Kırıcı route değişikliği yapılmamalı.

### P2 - Backend Kapalıyken Console 500 Logları

Durum:

- Backend kapalıyken sayfalar mock/default veriyle açılıyor.
- Ancak browser console'da API proxy 500 logları görülüyor.

Etkisi:

- Kullanıcı deneyimi kırılmıyor.
- Geliştirici deneyiminde console kirleniyor.

Çözüm planı:

- Kritik fetch çağrılarında hata yakalama zaten var; korunacak.
- İsteğe bağlı olarak UI içinde sessiz "demo veri kullanılıyor" durumu eklenebilir.
- Test ortamında backend down senaryosu ayrı kategori olarak kabul edilecek.

Kabul kriterleri:

- Backend kapalıyken dashboard, inventory, shipping, tasks, settings sayfaları crash etmemeli.
- Console logları kritik bug olarak değerlendirilmemeli, ama izlenmeli.

### P2 - NPM Audit Uyarıları

Durum:

- `next` üzerinden `postcss` için moderate seviyede uyarı var.
- Otomatik force fix kırıcı eski Next sürümü öneriyor.

Çözüm planı:

- `npm audit fix --force` uygulanmayacak.
- Next.js'in güvenli patch/minor sürüm güncellemesi araştırılacak.
- Gerekirse `overrides` ile güvenli `postcss` sürümü değerlendirilecek.
- Güncelleme sonrası `npm run build`, `npx tsc --noEmit` ve UI smoke tekrar koşulacak.

Kabul kriterleri:

- Kırıcı downgrade yapılmayacak.
- Audit uyarısı mümkünse güvenli şekilde kapatılacak.
- Uygulama build ve UI testleri geçmeye devam edecek.

## Geliştirme Planı

### Faz 1 - Kritik Auth Düzeltmesi

Amaç:

- Uygulamanın reload ve direkt link davranışını düzeltmek.

Yapılacaklar:

- `lib/auth.tsx` incelenecek.
- `AuthProvider` içine `authReady` state'i eklenecek.
- localStorage okuma try/catch ile güvenli hale getirilecek.
- Redirect effect'i `authReady` tamamlanmadan çalışmayacak.
- Login olmuş kullanıcı `/login`e giderse dashboard'a yönlendirilecek.
- Korumalı route açan oturumsuz kullanıcı login'e yönlendirilecek.

Testler:

- Direkt `/inventory` açılışı.
- Direkt `/shipping` açılışı.
- Direkt `/settings` açılışı.
- Logout sonrası `/shipping` açılışı.
- Bozuk localStorage manuel test.

### Faz 2 - Frontend Hata Mesajları

Amaç:

- Kullanıcıya API hatalarını anlaşılır ve Türkçe göstermek.

Yapılacaklar:

- Ortak hata mesajı helper'ı eklenecek.
- `app/inbox/page.tsx` Gemini hata okuma düzeltilecek.
- Gerekirse `settings`, `inventory`, `shipping` hata mesajları aynı helper'a yaklaştırılacak.

Testler:

- Gemini API key yokken taslak yenileme.
- Gemini 429 simülasyonu mümkünse backend seviyesinde.
- Integration test hata/simülasyon mesajları.

### Faz 3 - E2E ve Smoke Test Altyapısını Repo'ya Alma

Amaç:

- Bugün manuel/temporary çalışan testleri kalıcı hale getirmek.

Yapılacaklar:

- Playwright bağımlılığı ve scriptleri değerlendirmek.
- Minimum smoke test dosyası eklemek.
- Backend smoke testi için `pytest` veya basit Python script kararı vermek.
- Test komutlarını `package.json` veya dokümana eklemek.

Önerilen test komutları:

- `npm run build`
- `npx tsc --noEmit`
- Backend smoke
- Playwright UI smoke

Kabul kriterleri:

- Yeni geliştirici tek dokümandan testleri çalıştırabilmeli.
- Auth deep-link bug tekrar yakalanmalı.
- Inventory ve shipping crash regression tekrar yakalanmalı.

### Faz 4 - UX ve Tutarlılık İyileştirmeleri

Amaç:

- Demo uygulamayı daha profesyonel ve tutarlı hale getirmek.

Yapılacaklar:

- Modal input'larına erişilebilir label veya aria-label eklemek.
- Aynı işi yapan buton isimlerini tutarlılaştırmak.
- Entegrasyon modalında statik "Son test Bugün 14:32" bilgisini gerçek state'e bağlamak.
- Entegrasyon test sonucunu modal içinde de görünür hale getirmek.
- Bilgi tabanı route adını dokümanda netleştirmek veya redirect eklemek.
- Favicon/public asset eksikliğini gidermek.

Kabul kriterleri:

- Test selector'ları daha kararlı olmalı.
- Kullanıcı hangi entegrasyonun ne zaman test edildiğini görebilmeli.
- Browser favicon 404 üretmemeli.

### Faz 5 - Güvenlik ve Bağımlılık Hijyeni

Amaç:

- Audit uyarılarını kırıcı olmayan şekilde azaltmak.

Yapılacaklar:

- Next.js mevcut sürüm ağacı incelenecek.
- Güvenli patch/minor update denenebilir.
- `postcss` override stratejisi araştırılacak.
- Güncelleme sonrası build ve UI smoke tekrar koşulacak.

Kabul kriterleri:

- `npm audit --audit-level=moderate` mümkünse temizlenmeli.
- Temizlenemiyorsa gerekçe dokümante edilmeli.
- Force downgrade yapılmamalı.

## Sayfa Bazlı Test Bulguları

### Login

Çalışanlar:

- Varsayılan demo e-posta geliyor.
- Boş şifre validasyonu çalışıyor.
- 4+ karakter şifre ile giriş yapılabiliyor.
- Logout sonrası login'e dönüyor.

Geliştirilecek:

- Auth hydration sorunu nedeniyle direkt route açılışları bozuluyor.

### Dashboard

Çalışanlar:

- KPI kartları ve sağ bağlam paneli açılıyor.
- Son siparişler, görevler, fulfillment dağılımı ve son aktivite görünüyor.
- Backend kapalıyken default/mock veriyle açılıyor.

Geliştirilecek:

- Backend kapalıyken kullanıcıya opsiyonel demo veri göstergesi eklenebilir.

### Inbox

Çalışanlar:

- Konuşma seçimi çalışıyor.
- Bilgi tabanına ekleme modalı çalışıyor.
- Temsilciye devretme çalışıyor.
- Yanıt gönderme çalışıyor.
- Gemini key yokken crash olmadan hata toast'ı gösteriliyor.

Geliştirilecek:

- Gemini hata mesajı `detail` alanını doğru okumalı.
- "Taslağı Yenile" ve "Gemini ile Yenile" buton etiketleri tutarlılaştırılabilir.

### Kargo Takibi

Çalışanlar:

- Risk filtreleri çalışıyor.
- Satır seçimi sağ paneli güncelliyor.
- Proaktif bildirim simülasyonu çalışıyor.
- CSV raporu indiriliyor.
- Backend kapalı fallback çalışıyor.

Geliştirilecek:

- Bildirim başarısızlığı mesajları daha detaylı hale getirilebilir.
- Gerçek webhook modunda kısmi başarı/kısmi hata UI'da gösterilebilir.

### Stok Durumu

Çalışanlar:

- Satır seçimi çalışıyor.
- Stok düzenleme modalı çalışıyor.
- Tedarik siparişi verme çalışıyor.
- Tedarik taslağı simülasyonu çalışıyor.
- Kritik SKU CSV indiriliyor.
- Backend kapalı fallback çalışıyor.

Geliştirilecek:

- Panoya kopyalama fallback'i izin hatalarında ayrıca ele alınabilir.
- Tedarik aksiyonları için daha net "simülasyon modu" bilgisi verilebilir.

### Bilgi Tabanı

Çalışanlar:

- Arama çalışıyor.
- Kayıt ekleme çalışıyor.
- Kayıt silme çalışıyor.
- Backend kapalıyken sayfa crash etmiyor ve boş durum gösteriyor.

Geliştirilecek:

- Route adı `/knowledge-base` olarak dokümante edilmeli.
- Silme işlemine confirmation eklenebilir.

### Görevler

Çalışanlar:

- Görev ekleme çalışıyor.
- Görev tamamlama çalışıyor.
- Görev silme çalışıyor.
- Sağ bağlam paneli seçili görevi gösteriyor.

Geliştirilecek:

- Form inputlarına placeholder veya aria-label eklenebilir.
- Görev silme için confirmation eklenebilir.

### Ayarlar

Çalışanlar:

- Kullanıcı ekleme çalışıyor.
- Rol güncelleme çalışıyor.
- Entegrasyon sekmesi çalışıyor.
- Entegrasyon test butonu çalışıyor.
- Entegrasyon ayar modalı açılıyor.
- Bildirim tercihleri kaydediliyor.

Geliştirilecek:

- Entegrasyon modalındaki son test zamanı statik.
- Test sonucunun modal içinde kalıcı görünmesi iyi olur.
- Kullanıcı aktif/pasif işleminde kendi admin hesabını kapatma riskine karşı koruma eklenebilir.

## Sonraki Uygulama Sırası

Önerilen sıra:

1. P0 auth hydration/deep-link düzeltmesi
2. Gemini/API hata mesajı helper'ı
3. Kısa regression test turu
4. Test altyapısını repo'ya alma
5. UX tutarlılık düzeltmeleri
6. Audit/bağımlılık hijyeni

İlk geliştirme turunda sadece 1 ve 2 numaralı maddeleri yapmak en güvenli adımdır. Bunlar kullanıcı deneyimini doğrudan etkileyen ve testle net yakalanan gerçek sorunlardır.

## Tekrar Çalıştırılacak Kabul Testleri

Her önemli düzeltmeden sonra aşağıdaki kontroller çalıştırılmalı:

- `npx tsc --noEmit`
- `npm run build`
- Backend smoke test
- Production UI smoke test
- Backend kapalı fallback smoke test

Özellikle auth düzeltmesinden sonra tekrar kontrol edilecekler:

- Login başarılı.
- `/inventory` direkt açılıyor.
- `/shipping` direkt açılıyor.
- `/settings` direkt açılıyor.
- Logout sonrası korumalı route login'e gidiyor.
- Bozuk localStorage crash üretmiyor.

## Notlar

- Test sırasında `3010` portunda bu repodan çalışan mevcut bir Node/Next süreci görüldü. Ona dokunulmadı.
- Testler çakışmayı önlemek için farklı port üzerinde çalıştırıldı.
- Test süreçleri sonunda backend/frontend süreçleri kapatıldı.
- `.env.local` içeriği değiştirilmedi ve bu dokümana gizli değer yazılmadı.
- In-memory veri yaklaşımı bu demo fazı için bilinçli kabul olarak devam ediyor.
