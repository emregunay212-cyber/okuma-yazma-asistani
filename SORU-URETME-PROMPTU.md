# Soru Üretme Promptu (Test/QA)

> Aşağıdaki metni, **PROJE-TANITIMI.md** dosyasıyla birlikte başka bir yapay zekaya
> ver. Önce tanıtım dosyasını yapıştır/yükle, sonra bu promptu gönder.

---

## KOPYALANACAK PROMPT (buradan aşağısı)

Sana yukarıda tanıttığım **"Okuma Yazma Asistanım"** uygulaması için **test/QA
soruları** üretmeni istiyorum. Amaç: asistanın deterministik cevap katmanını,
soru-algılama (FAQ eşleşme) mantığını ve konu-dışı kapısını **kırmaya çalışan**,
çeşitli ve zorlayıcı bir test seti oluşturmak. Asistanı methetmek değil, **hata
çıkaracak** sorular üret.

### Üreteceğin her test sorusu için tam olarak şu alanları doldur:

| Alan | Açıklama |
|------|----------|
| **soru** | Kullanıcının (1-2. sınıf çocuk veya veli) yazacağı metin, aynen. |
| **kategori** | Hangi konu: heceleme / harf sayımı / sesli-sessiz / ilk-son harf / imla / noktalama / büyük harf / alfabe / dikte / FAQ-kural / konu-dışı |
| **beklenen_katman** | `deterministik` (1) / `konu-dışı yönlendirme` (2) / `model` (3) |
| **beklenen_cevap** | TDK'ye göre **doğru** kısa cevap (heceleme/sayım sorularında kesin değer yaz). |
| **zorluk** | `kolay` / `orta` / `tuzak` |
| **neden_tuzak** | (tuzak ise) Bu sorunun hangi kırılganlığı hedeflediği. |

### Çıktı formatı
Markdown tablosu **veya** JSON dizisi olarak ver (ikisinden birini seç, tutarlı ol).
JSON tercih edersen şu şekilde:

```json
[
  {
    "soru": "kelebek hecele",
    "kategori": "heceleme",
    "beklenen_katman": "deterministik",
    "beklenen_cevap": "ke-le-bek (3 hece)",
    "zorluk": "kolay",
    "neden_tuzak": ""
  }
]
```

### Üretim kuralları
1. **Toplam ~60 soru** üret, kategorilere dengeli dağıt.
2. En az **%40'ı `tuzak`** olsun. Tuzaklar şunları hedeflesin:
   - **Yanlış kelime yakalama:** Cümlede birden çok kelime varken sistemin yanlış
     kelimeyi hecelemesi/sayması (örn. "kitap mı kalem mi daha uzun").
   - **Aksan-duyarsızlık:** Türkçe karaktersiz yazım ("kac harf", "unlu mu",
     "buyuk harf", "virgul nereye") — doğru yakalanmalı ama yanlış kelime DEĞİL.
   - **Niyet sınırı:** "de/da", "ki", "mi" eklerinin ve imla düzeltmelerinin
     yalnızca **yazım niyeti** olduğunda tetiklenmesi gerektiği — günlük cümlede
     ("Ali de geldi", "film nasıl çekilir") tetiklenmemeli.
   - **Zor sayımlar:** "ğ", "ı/i", çift ünsüz içeren kelimeler ("yağmur", "ışık",
     "iğne", "kitapçı") — harf/hece/sesli-sessiz sayımı doğru mu?
   - **Konu-dışı sızıntı:** Konu-dışı bir sorunun, içinde "oku", "yaz", "ses" gibi
     bir anahtar kelime geçtiği için yanlışlıkla modele gitmesi.
   - **Yanlış red:** Geçerli bir okuma-yazma sorusunun, anahtar kelime içermediği
     için haksızca "konu-dışı" sayılması.
   - **Sınır girdileri:** Tek harf, çok uzun kelime, sayı, sadece noktalama,
     boş/anlamsız metin, fazladan boşluk, büyük-küçük harf karışık.
3. Sorular **gerçekçi** olsun — bir çocuğun veya velinin gerçekten yazacağı dilde
   (yazım hataları, eksik Türkçe karakter, kısa ifadeler dahil).
4. **Beklenen cevapları sen TDK'ye göre doğru hesapla.** Heceleme: her hecede bir
   ünlü; iki ünlü arası tek ünsüz sonraki heceye; iki ünsüz bölünür. Sesli (8):
   a e ı i o ö u ü. Sessiz (21): b c ç d f g ğ h j k l m n p r s ş t v y z.
   Alfabe: 29 harf.
5. Aynı soruyu tekrarlama; ifade ve kelime çeşitliliği yüksek olsun.

Önce kısa bir **kapsam tablosu** ver (her kategoriden kaç soru, kaç tuzak),
sonra soruların tam listesini üret.
