# Okuma Yazma Asistanım — Proje Tanıtımı (Test Üretimi İçin)

> Bu belge, başka bir yapay zekaya projeyi tanıtmak ve ona **test/QA soruları**
> ürettirmek için hazırlanmıştır. Aşağıdaki bilgiler, asistanın nasıl çalıştığını,
> hangi katmanların hangi soruları yakaladığını ve nerelerde **kırılgan** olduğunu
> anlatır. Test üreten yapay zeka, bu kırılganlıkları hedef alarak soru üretmelidir.

---

## 1. Proje Nedir?

**Hedef kitle:** 1. ve 2. sınıf ilkokul öğrencileri (ilk okuma-yazma öğrenenler).

**Amaç:** Türkçe okuma-yazma konularında (harfler, sesler, alfabe, heceleme,
kelimeler, cümleler, imla/yazım, noktalama) TDK (Türk Dil Kurumu) kurallarına
**tam uyumlu**, çocuk dostu, kısa ve sevecen cevaplar veren bir sohbet asistanı.

**Teknik yapı:** Tek dosyalık bir web uygulaması (`okuma-yazma-asistani.html`) —
vanilla HTML/CSS/JavaScript. Sunucu tarafında Vercel serverless proxy
(`api/gemini.js`) yapay zeka anahtarını saklar. Ayrıca dört eğitsel oyun içerir
(Hece Bul, Sesli mi Sessiz mi, Kelimeyi Tamamla, Hece Sayısı).

> **Önemli not:** `README.md` "Anthropic Claude Haiku" yazsa da, koddaki gerçek
> model **Google Gemini 2.5 Flash Lite**'tır (`gemini-2.5-flash-lite`). Bu bir
> dokümantasyon tutarsızlığıdır; test açısından önemli olan koddaki davranıştır.

---

## 2. Cevap Akışı — 3 Katman (EN ÖNEMLİ BÖLÜM)

Kullanıcı bir mesaj gönderdiğinde sırayla şu katmanlardan geçer
(`chat()` fonksiyonu, `okuma-yazma-asistani.html`):

```
Kullanıcı sorusu
   │
   ▼
[1] DETERMİNİSTİK KATMAN  (localAnswer)
   │  Model gerektirmez, her zaman doğru, internetsiz de çalışır.
   │  Eşleşirse → cevabı döndür, DUR.
   │  Eşleşmezse → aşağı in.
   ▼
[2] KONU-DIŞI KAPISI  (onTopic)
   │  Soru okuma-yazmayla ilgili değilse →
   │  "Ben okuma-yazma asistanıyım 😊 ..." yönlendirmesi, DUR.
   │  (API'ye GİTMEZ.)
   ▼
[3] MODEL FALLBACK  (Gemini 2.5 Flash Lite)
      Yukarıdakilere takılmayan serbest sorular modele gider.
      Sistem promptu TDK kuralları + çocuk dostu üslup + konu kısıtı dayatır.
```

**Test ederken her soru için beklenen davranış şudur:**
hangi katmanın yakalaması gerektiği ve verilen cevabın TDK'ye uygun olup olmadığı.
En kritik hatalar **[1] katmanının yanlış eşleşmesi** (yanlış kelimeyi yakalama,
yanlış sayım) veya **[2] katmanının yanlış yönlendirmesidir** (geçerli okuma-yazma
sorusunu konu-dışı sayma ya da konu-dışı soruyu modele kaçırma).

---

## 3. Deterministik Katman Ne Yakalar? (localAnswer)

Bu katman regex + algoritma ile çalışır. Türkçe karakterler **aksan-duyarsız**
eşleşir: `ç→c, ğ→g, ı→i, ö→o, ş→s, ü→u` (yani "kac harf", "buyuk", "unlu",
"virgul" gibi Türkçe karaktersiz yazımlar da yakalanır).

Sırasıyla yakaladıkları:

| # | Soru tipi | Örnek girdi | Beklenen cevap |
|---|-----------|-------------|----------------|
| 0a | Kelimenin **ilk harfi** | `kalem kelimesinin ilk harfi nedir` | `K` |
| 0b | Kelimenin **son harfi** | `okul son harf` | `L` |
| 0c | Kelimede **kaç sessiz** | `çiçek kaç sessiz` | 2 |
| 0d | Kelimede **kaç sesli** | `kalem kaç sesli` | 2 |
| 0e | Kelimede **kaç harf** | `araba kaç harf` | 5 |
| 1  | Tek bir **harfin türü** | `b harfi sesli mi`, `a sesli mi` | sessiz / sesli |
| 2  | **Sesli/sessiz harf listesi** | `sesli harfler neler` | 8 ünlü listesi |
| 3  | **FAQ bankası** (kural/kavram) | `de da nasıl yazılır`, `herkez mi herkes mi` | bankadaki hazır cevap |
| 4  | **Heceleme** | `kelebek hecele`, `araba kaç hece` | ke-le-bek (3) |
| 5  | **Alfabe / kaç harf** | `alfabede kaç harf var` | 29 (8+21) |
| 6  | **Büyük harf** kuralı | `büyük harf ne zaman` | cümle başı + özel isim |
| 7  | **Noktalama** (nokta, virgül, soru işareti, ünlem) | `virgül nereye konur` | kural + örnek |
| 8  | **İmla** (genel) | `imla kuralları` | kısa kural listesi |
| 9  | **Dikte** kelimeleri | `bana dikte kelimeleri ver` | rastgele 10 kelime |

### Heceleme algoritması (TDK)
- Her hecede **bir sesli (ünlü)** harf vardır. **Hece sayısı = ünlü sayısı.**
- İki ünlü arasındaki **tek ünsüz** sonraki heceye gider: `a-ra-ba`, `ka-pı`.
- Yan yana **iki ünsüz** bölünür: `el-ma`, `kar-tal`, `çan-ta`.
- Heceler birleşince kelime AYNEN çıkmalı (harf eklenmez/çıkarılmaz).

### Sayımlar
- Sesli harfler (8): `a e ı i o ö u ü`
- Sessiz harfler (21): `b c ç d f g ğ h j k l m n p r s ş t v y z`
- Türk alfabesi: 29 harf.

---

## 4. FAQ Bankası Eşleşme Mantığı (kritik kırılganlık kaynağı)

Banka `gen_faq.py` ile üretilir → `faq.js` (`window.OW_FAQ` dizisi, ~1658 kayıt).
Her kayıt şu alanlara sahiptir ve eşleşme **aksan-duyarsız** yapılır:

- **`w`** (word): Hedef kelime. Soruda **tam kelime** olarak geçmeli (kelime sınırıyla).
- **`k`** (keywords): Listedeki **TÜM** alt dizeler soruda geçmeli (intent/niyet).
- **`kany`** (keywords-any): Listedeki **en az biri** geçmeli.
- Eşleşen kayıtlar arasından **en uzun/en spesifik** olan seçilir (skor).

**Bu mekanizma neden kırılgan?** Test üretirken özellikle şunları zorla:
- Bir kelimenin yanlışlıkla başka bir bankadaki cevabı tetiklemesi.
- "bir" gibi kelimeler `STOP_WORDS`'tedir (hem sayı hem artikel olduğu için
  "bir kelimede kaç harf" sorusunda yanlış eşleşmesin diye çıkarılmıştır).
- İmla düzeltmeleri yalnızca **yazım niyeti** (`yaz, ayrı, bitişik, imla`) varsa
  tetiklenir — yani "film nasıl çekilir" gibi sorularda yanlışça "film" düzeltmesi
  çıkmamalı. Test bu sınırı yokla.
- "de/da", "ki", "mi" gibi ekler yalnızca yazım/kural niyetiyle eşleşmeli;
  günlük cümlede ("Ali de geldi") tetiklenmemeli.

---

## 5. Konu-Dışı Kapısı (onTopic)

Deterministik katman boş dönerse, soru şu anahtar kelimelerden **en az birini**
içermiyorsa **konu-dışı** sayılır ve modele gönderilmeden yönlendirme mesajı verilir:

```
harf, ses, ünlü, ünsüz, alfabe, hece, kelime, sözcük, cümle, imla,
yazım, yaz, oku, dikte, nokta, virgül, noktalama, ünlem, vurgu,
satır, şiir, tekerleme, metin, paragraf, türkçe
```

**Yönlendirme mesajı:**
> "Ben okuma-yazma asistanıyım 😊 Sana harfler, heceler, kelimeler, cümleler ve
> yazım konularında yardımcı olabilirim. Bunlardan birini sormak ister misin?"

**Test açısından iki hata tipi:**
1. **Yanlış pozitif (kaçak):** Konu-dışı bir soru bu kelimelerden birini içerdiği
   için modele gider. Örn: "futbol **maç**ı ne zaman" → "maç" içinde "**aç**" yok
   ama "**oku**lda maç" gibi bir cümle "oku" yüzünden geçebilir. Bu tür sızıntıları ara.
2. **Yanlış negatif:** Geçerli bir okuma-yazma sorusu bu kelimelerin hiçbirini
   içermediği için haksızca konu-dışı sayılır.

---

## 6. Model Katmanı — Sistem Promptu Kuralları

Modele düşen sorularda sistem promptu şunları dayatır (test ederken model
cevaplarının bunlara uyup uymadığı kontrol edilmeli):

- **Kapsam kısıtı:** Yalnızca okuma-yazma konuları. Konu dışıysa SADECE
  yönlendirme cümlesini söylemeli; bilgi vermemeli, tahmin yürütmemeli.
- **TDK uyumu:** Heceleme, sesli/sessiz sayıları, özel isim yazımı tam doğru.
- **Üslup:** En fazla 3-4 cümle, sade, sevecen, bol örnek, az teori, olumsuz dil yok.
- **Türkçe karakter doğruluğu:** i/ı, o/ö, u/ü, c/ç, g/ğ, s/ş ayrı harfler;
  özel isimler doğru yazılmalı (Ali, İzmir, Türkiye).

---

## 7. Test Üretirken Özellikle Zorlanması Gereken Noktalar

1. **Yanlış kelime yakalama:** Cümlede birden çok kelime varken yanlış kelimenin
   hecelenmesi/sayılması (örn. "kitap mı kalem mi daha uzun").
2. **Aksan-duyarsızlık tuzakları:** "kac harf", "unlu sessiz", "buyuk harf"
   yazımlarının doğru yakalanması; ama yanlış kelimeyi de yakalamaması.
3. **Niyet sınırları:** İmla düzeltmeleri ve de/da/ki/mi'nin yalnızca yazım
   niyetiyle tetiklenmesi; günlük cümlede tetiklenmemesi.
4. **Sayım doğruluğu:** "ğ", "ı/i" gibi harfler içeren kelimelerde harf/hece/
   sesli-sessiz sayımının doğru olması (örn. "yağmur", "ışık", "iğne").
5. **Konu-dışı sızıntı/yanlış red:** onTopic kapısının iki yönlü hataları.
6. **Sınır/aykırı girdiler:** Tek harf, çok uzun kelime, sayı, noktalama yığını,
   boş/anlamsız metin, büyük-küçük harf karışık, fazladan boşluk.
