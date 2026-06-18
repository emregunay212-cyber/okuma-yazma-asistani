# 📚 Okuma Yazma Asistanım

1. ve 2. sınıf ilkokul öğrencilerine yönelik, yapay zeka destekli Türkçe okuma yazma yardımcısı.

---

## 🎯 Proje Hakkında

Bu uygulama, ilk okuma yazma öğrenen çocuklara harfler, heceler, imla kuralları ve noktalama işaretleri konularında seviyelerine uygun, TDK kurallarına tam uyumlu rehberlik sağlar. Anthropic'in Claude yapay zeka modeli ile çalışır.

---

## ✨ Özellikler

### 💬 Yapay Zeka Sohbeti
- Çocuk dostu, sade ve sevecen dil
- TDK Yazım Kılavuzu kurallarına tam uyum
- Kısa ve anlaşılır yanıtlar (çocukları yormaz)
- Hızlı yanıt için Claude Haiku modeli kullanılır

### 📖 Konu Modları
| Konu | İçerik |
|------|--------|
| 💬 Serbest Soru | Her türlü okuma yazma sorusu |
| 🔤 Harfler ve Sesler | Sesli-sessiz harf, alfabe |
| ✂️ Hece Bölme | Hece kuralları ve örnekler |
| 📝 İmla Kuralları | Büyük harf, birleşik-ayrı yazım |
| ❓ Noktalama | Nokta, virgül, soru işareti, ünlem |
| ✏️ Dikte Kelimeleri | Sınıfa göre kelime listeleri |

### 🎮 Oyunlar
| Oyun | Açıklama |
|------|----------|
| ✂️ Hece Bul | Kelimenin doğru hece bölümünü 4 seçenekten seç |
| 🔊 Sesli mi Sessiz mi? | Verilen harfi doğru sınıflandır |
| 🔤 Kelimeyi Tamamla | Eksik harfi bulup yaz |
| 🔢 Hece Sayısı | Kelimedeki hece sayısını bul |

Her oyunda **doğru / toplam / başarı yüzdesi** takip edilir.

---

## 🚀 Kurulum

### Gereksinimler
- Modern bir web tarayıcısı (Chrome, Edge, Firefox, Safari)
- Anthropic API anahtarı
- İnternet bağlantısı

### Çalıştırma
1. `okuma-yazma-asistani.html` dosyasını indir
2. Dosyaya çift tıkla — tarayıcıda açılır
3. İlk açılışta API anahtarı giriş ekranı gelir
4. Anahtarı gir ve **Kaydet** butonuna tıkla
5. Uygulama kullanıma hazır ✅

> API anahtarı tarayıcıya kaydedilir, bir daha sorulmaz.

---

## 🔑 API Anahtarı Alma

1. [console.anthropic.com](https://console.anthropic.com) adresine git
2. Ücretsiz hesap oluştur
3. **API Keys** → **Create Key** butonuna tıkla
4. `sk-ant-...` ile başlayan anahtarı kopyala
5. Uygulamada ilgili alana yapıştır

> ⚠️ API anahtarını kimseyle paylaşma. Yanlışlıkla paylaştıysan hemen [console.anthropic.com](https://console.anthropic.com) adresinden sil ve yenisini oluştur.

---

## 🛠️ Teknik Detaylar

### Dosya Yapısı
```
okuma-yazma-asistani.html   ← Tek dosya, her şey içinde
```

Uygulama tek bir HTML dosyasından oluşur. CSS ve JavaScript ayrı dosyalara gerek yoktur.

### Kullanılan Teknolojiler
| Teknoloji | Kullanım |
|-----------|----------|
| HTML5 / CSS3 | Arayüz |
| Vanilla JavaScript | Uygulama mantığı |
| Anthropic API | Yapay zeka yanıtları |
| Claude Haiku | Hızlı model (düşük gecikme) |
| Google Fonts — Nunito | Çocuk dostu yazı tipi |
| localStorage | API anahtarı saklama |

### API Ayarları
```
Model     : claude-haiku-4-5-20251001
Max Tokens: 400
```
Haiku modeli ve düşük token limiti, yanıt hızını önemli ölçüde artırır.

---

## 📐 TDK Kural Kapsamı

Uygulama aşağıdaki TDK kurallarını öğretir ve uygular:

- **Büyük harf:** Cümle başı, özel isimler (kişi, şehir, ülke, ırmak, dağ), unvanlar
- **Noktalama:** Nokta, virgül, soru işareti, ünlem, iki nokta, kesme işareti
- **Hece bölme:** Sesli harf kuralı, iki sessiz yan yana bölme, satır sonu tire
- **Sesli harfler:** a, e, ı, i, o, ö, u, ü (8 adet)
- **Sessiz harfler:** b, c, ç, d, f, g, ğ, h, j, k, l, m, n, p, r, s, ş, t, v, y, z (21 adet)
- **Birleşik yazım:** Doğru birleşik ve ayrı yazım örnekleri

---

## 🎨 Tasarım

- Mobil uyumlu (responsive) tasarım
- Hamburger menü (küçük ekranlar için)
- Çocuk dostu yuvarlak köşeler ve pastel renkler
- Mor (#534AB7) ve yeşil (#1D9E75) ana renk paleti
- Animasyonlu yazma göstergesi (üç nokta)

---

## 🔒 Güvenlik

- API anahtarı yalnızca kullanıcının kendi tarayıcısında saklanır
- Sunucuya hiçbir kişisel veri gönderilmez
- Tüm yapay zeka istekleri doğrudan Anthropic API'sine yapılır

---

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir. Serbestçe kullanılabilir ve geliştirilebilir.

---

*Anthropic Claude ile güçlendirilmiştir.*
