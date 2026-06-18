# Okuma Yazma Asistanı — Test/QA Soru Seti

> Toplam **287** soru. Her soru sistemin GERÇEK mantığından (`test/sim.py` — `localAnswer`+`onTopic`+`faqLookup`'un birebir Python portu) geçirilmiştir; `beklenen` (TDK-doğru/ideal davranış) ile `gerçek` (sistemin fiilen yaptığı) karşılaştırılır.

> **Geçen (OK): 261/287** · **Uyuşmazlık: 26** (bunların 15 tanesi CİDDİ: yanlış değer / yanlış red / sızıntı).


## Özet

| Zorluk | Adet |
|--------|------|
| kolay | 98 |
| orta | 85 |
| tuzak | 104 |

| Durum | Adet | Anlamı |
|-------|------|--------|
| OK | 261 | beklenen = gerçek |
| YANLIŞ-RED | 2 | Geçerli soru haksızca konu-dışına yönlendirildi |
| SIZINTI | 13 | Konu-dışı olması gereken soru cevaplandı/modele gitti |
| DET-FAZLA | 8 | Model beklenirken deterministik tetiklendi (yanlış-kelime yakalama riski — incele) |
| DET-KAÇIŞ | 3 | Deterministik beklenirken modele düştü (kapsam açığı; model yine yanıtlar) |

| Kategori | Adet | Uyuşmazlık |
|----------|------|------------|
| heceleme | 52 | 0 |
| harf sayımı | 24 | 0 |
| sesli-sessiz | 32 | 0 |
| ilk-son harf | 17 | 0 |
| yanlış-kelime yakalama | 26 | 9 |
| imla | 26 | 0 |
| noktalama | 18 | 3 |
| büyük harf | 10 | 0 |
| alfabe | 10 | 0 |
| FAQ-kural | 25 | 1 |
| konu-dışı | 30 | 12 |
| sınır/aykırı girdiler | 17 | 1 |

## ⚠️ Bulgular (sistem ideal davranıştan sapıyor)

Önem sırasına göre gruplanmıştır. CİDDİ olanlar gerçek bug adayıdır; DET-KAÇIŞ/DET-FAZLA çoğu zaman tartışmalıdır (model yine doğru yanıtlayabilir).


### YANLIŞ-RED — Geçerli soru haksızca konu-dışına yönlendirildi (2)

| # | Soru | Beklenen | Gerçek | Gerçek cevap (kısalt.) |
|---|------|----------|--------|------------------------|
| 1 | `kitap mı kalem mi daha uzun` | model | konu-dışı yönlendirme | Ben okuma-yazma asistanıyım 😊 Sana harfler, heceler, ke |
| 2 | `hangisi daha kısa kapı yoksa pencere` | model | konu-dışı yönlendirme | Ben okuma-yazma asistanıyım 😊 Sana harfler, heceler, ke |

### SIZINTI — Konu-dışı olması gereken soru cevaplandı/modele gitti (13)

| # | Soru | Beklenen | Gerçek | Gerçek cevap (kısalt.) |
|---|------|----------|--------|------------------------|
| 1 | `bana dokunma!` | konu-dışı yönlendirme | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |
| 2 | `yazılım mühendisi ne iş yapar?` | konu-dışı yönlendirme | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |
| 3 | `yeni yazıcı aldık ama çalışmıyor` | konu-dışı yönlendirme | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |
| 4 | `abimin ses tonu çok kalın` | konu-dışı yönlendirme | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |
| 5 | `gece her yer sessizlik içindeydi` | konu-dışı yönlendirme | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |
| 6 | `Metin dayım bize hediye getirdi` | konu-dışı yönlendirme | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |
| 7 | `basketbolda nokta atışı yaptım` | konu-dışı yönlendirme | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |
| 8 | `yarın sınavda yazıyoruz, çok heyecanlıyım` | konu-dışı yönlendirme | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |
| 9 | `yaz gelince denize gireceğiz` | konu-dışı yönlendirme | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |
| 10 | `midemde garip bir vurgu hissettim` | konu-dışı yönlendirme | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |
| 11 | `babam yazıhanede çalışıyor` | konu-dışı yönlendirme | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |
| 12 | `bu yaz çok sıcak olacak galiba` | konu-dışı yönlendirme | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |
| 13 | `12345 kaç harf` | konu-dışı yönlendirme | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |

### DET-FAZLA — Model beklenirken deterministik tetiklendi (yanlış-kelime yakalama riski — incele) (8)

| # | Soru | Beklenen | Gerçek | Gerçek cevap (kısalt.) |
|---|------|----------|--------|------------------------|
| 1 | `hece ne demek` | model | deterministik | Hece bölme kuralı: Her hecede bir sesli harf vardır. İk |
| 2 | `annemin adını hecele` | model | deterministik | adını → a - dı - nı (3 hece) 😊 |
| 3 | `benim adım kaç harf` | model | deterministik | adım kelimesinde 4 harf vardır. 😊 |
| 4 | `kelime kaç hecelidir` | model | deterministik | Hece bölme kuralı: Her hecede bir sesli harf vardır. İk |
| 5 | `bir kelime kaç hece içerir` | model | deterministik | Hece bölme kuralı: Her hecede bir sesli harf vardır. İk |
| 6 | `okul kelimesi kaç harf kitap kelimesi kaç harf` | model | deterministik | kitap kelimesinde 5 harf vardır. 😊 |
| 7 | `adının ilk harfi ne benim` | model | deterministik | adının kelimesinin ilk harfi A harfidir. 😊 |
| 8 | `bana bir kelime hecele` | model | deterministik | Hece bölme kuralı: Her hecede bir sesli harf vardır. İk |

### DET-KAÇIŞ — Deterministik beklenirken modele düştü (kapsam açığı; model yine yanıtlar) (3)

| # | Soru | Beklenen | Gerçek | Gerçek cevap (kısalt.) |
|---|------|----------|--------|------------------------|
| 1 | `öğretmenim bugün hava güzel cümlesinin sonuna ne koymalıyım` | deterministik | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |
| 2 | `Ali de geldi cümlesinde virgül var mı` | deterministik | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |
| 3 | `nokta ile virgül arasındaki fark ne` | deterministik | model | [MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre y |

## Tam Soru Listesi


### heceleme (52)

| Soru | Beklenen katman | Beklenen cevap | Zorluk | Gerçek katman | Durum | Tuzak nedeni |
|------|-----------------|----------------|--------|---------------|-------|--------------|
| elma hecele | deterministik | elma → el-ma (2 hece) | kolay | deterministik | ✅ |  |
| kitap kelimesini hecele | deterministik | kitap → ki-tap (2 hece) | kolay | deterministik | ✅ |  |
| kalem kaç hecelidir? | deterministik | 2 hece: ka-lem | kolay | deterministik | ✅ |  |
| okul hecele | deterministik | okul → o-kul (2 hece) | kolay | deterministik | ✅ |  |
| masa kelimesini hecele | deterministik | masa → ma-sa (2 hece) | kolay | deterministik | ✅ |  |
| kapı kaç hecelidir? | deterministik | 2 hece: ka-pı | kolay | deterministik | ✅ |  |
| arı hecele | deterministik | arı → a-rı (2 hece) | kolay | deterministik | ✅ |  |
| çiçek kelimesini hecele | deterministik | çiçek → çi-çek (2 hece) | kolay | deterministik | ✅ |  |
| bulut kaç hecelidir? | deterministik | 2 hece: bu-lut | kolay | deterministik | ✅ |  |
| tavuk hecele | deterministik | tavuk → ta-vuk (2 hece) | kolay | deterministik | ✅ |  |
| kelebek kelimesini hecele | deterministik | kelebek → ke-le-bek (3 hece) | kolay | deterministik | ✅ |  |
| karpuz kaç hecelidir? | deterministik | 2 hece: kar-puz | kolay | deterministik | ✅ |  |
| limon hecele | deterministik | limon → li-mon (2 hece) | kolay | deterministik | ✅ |  |
| balık kelimesini hecele | deterministik | balık → ba-lık (2 hece) | kolay | deterministik | ✅ |  |
| yağmur kaç hecelidir? | deterministik | 2 hece: yağ-mur | orta | deterministik | ✅ |  |
| ışık hecele | deterministik | ışık → ı-şık (2 hece) | orta | deterministik | ✅ |  |
| iğne kelimesini hecele | deterministik | iğne → iğ-ne (2 hece) | orta | deterministik | ✅ |  |
| kitapçı kaç hecelidir? | deterministik | 3 hece: ki-tap-çı | orta | deterministik | ✅ |  |
| gökyüzü hecele | deterministik | gökyüzü → gök-yü-zü (3 hece) | orta | deterministik | ✅ |  |
| ağaç kelimesini hecele | deterministik | ağaç → a-ğaç (2 hece) | orta | deterministik | ✅ |  |
| şemsiye kaç hecelidir? | deterministik | 3 hece: şem-si-ye | orta | deterministik | ✅ |  |
| uçak hecele | deterministik | uçak → u-çak (2 hece) | orta | deterministik | ✅ |  |
| oyuncak kelimesini hecele | deterministik | oyuncak → o-yun-cak (3 hece) | orta | deterministik | ✅ |  |
| sınıf kaç hecelidir? | deterministik | 2 hece: sı-nıf | orta | deterministik | ✅ |  |
| ağustos hecele | deterministik | ağustos → a-ğus-tos (3 hece) | orta | deterministik | ✅ |  |
| kütüphane kelimesini hecele | deterministik | kütüphane → kü-tüp-ha-ne (4 hece) | orta | deterministik | ✅ |  |
| bilgisayar kaç hecelidir? | deterministik | 4 hece: bil-gi-sa-yar | orta | deterministik | ✅ |  |
| televizyon hecele | deterministik | televizyon → te-le-viz-yon (4 hece) | orta | deterministik | ✅ |  |
| öğretmen kelimesini hecele | deterministik | öğretmen → öğ-ret-men (3 hece) | orta | deterministik | ✅ |  |
| yoğurt kaç hecelidir? | deterministik | 2 hece: yo-ğurt | orta | deterministik | ✅ |  |
| karpuz kaç hece | deterministik | 2 hece: kar-puz | orta | deterministik | ✅ |  |
| kütüphane kaç hece | deterministik | 4 hece: kü-tüp-ha-ne | orta | deterministik | ✅ |  |
| şemsiye kaç hece | deterministik | 3 hece: şem-si-ye | orta | deterministik | ✅ |  |
| yağmur kaç hece | deterministik | 2 hece: yağ-mur | orta | deterministik | ✅ |  |
| yağmur kelimesini heceler misin | deterministik | yağmur kelimesini doğru hecelemeli ve hece sayısın | kolay | deterministik | ✅ | Doğal nazik ifade ('heceler misin') ama 'yağmur' hecele'den hemen önce |
| ışık nasıl hecelenir | deterministik | İdeal: 'ışık' kelimesini hecelemeli. Gerçekte rege | tuzak | deterministik | ✅ | 'X nasıl hecelenir' kalıbında araya 'nasıl' girer; regex hedefi 'nasıl |
| şemsiye nasıl hecelenir | deterministik | İdeal: 'şemsiye' hecelenmeli. Gerçekte hedef 'nası | tuzak | deterministik | ✅ | 'nasıl hecelenir' kalıbı hedefi 'nasıl'a kaydırır; banka dışı 'şemsiye |
| Kitap nasıl hecelenir | deterministik | İdeal: 'kitap' hecelenmeli. Gerçekte hedef 'nasıl' | tuzak | deterministik | ✅ | Büyük harf + 'nasıl hecelenir' kalıbı birleşince hedef yine 'nasıl'a k |
| kitabı hecele | deterministik | Yakalanan hedef ek almış 'kitabı' olur; 'kitabı' k | tuzak | deterministik | ✅ | Ek almış kelime: hedef kök 'kitap' yerine 'kitabı' olur; çocuk kökü be |
| yağmuru hecele | deterministik | Hedef ek almış 'yağmuru' olur; 'yağmuru' kelimesin | tuzak | deterministik | ✅ | Belirtme eki almış kelime hedef olur; kök 'yağmur' değil 'yağmuru' hec |
| ağacı kaç hece | deterministik | Hedef ek almış 'ağacı' olur; 'ağacı' kelimesinin h | tuzak | deterministik | ✅ | Ek almış kelime + yumuşama (ağaç→ağacı) hedef olur; kök ile farklı hec |
| uçağı hecele | deterministik | Hedef ek almış 'uçağı' olur; 'uçağı' kelimesini do | tuzak | deterministik | ✅ | Yumuşama + ek (uçak→uçağı) ile hedef kökten farklılaşır; çocuk kökü be |
| ağustos böceği kaç hece | deterministik | İdeal: 'ağustos' (veya tüm öbek) için cevap. Gerçe | tuzak | deterministik | ✅ | İki kelimelik öbekte regex yalnız son kelimeyi ('böceği') yakalar; ban |
| kitapçı kaç hece | deterministik | kitapçı kelimesinin hece sayısını vermeli. | orta | deterministik | ✅ | Banka dışı türemiş kelime (kitap+çı); kökten farklı, doğru çekimsiz tü |
| ağaç kelimesini heceler misin | deterministik | ağaç kelimesini doğru hecelemeli ve hece sayısını  | kolay | deterministik | ✅ | Doğal soru kalıbı; 'ağaç' 'kelimesini'den önce olduğu için hedef doğru |
| uçak kaç heceli | deterministik | uçak kelimesinin hece sayısını vermeli. | kolay | deterministik | ✅ | 'heceli' içindeki 'hece' yakalanır; banka dışı kelime, sesli ile başla |
| oyuncak hecele | deterministik | oyuncak kelimesini doğru hecelemeli ve hece sayısı | orta | deterministik | ✅ | Banka dışı; 'oy' ile başlama ve 'nc' sessiz çifti hece bölme kuralını  |
| sınıf hecele | deterministik | sınıf kelimesini doğru hecelemeli ve hece sayısını | orta | deterministik | ✅ | Banka dışı; 'sınıf' iki sesli (ı-ı) arası tek sessiz (n) sonraki hecey |
| ağustos kelimesini hecele | deterministik | ağustos kelimesini doğru hecelemeli ve hece sayısı | orta | deterministik | ✅ | Banka dışı; 'ğ' ve 'st' sessiz çifti ile uzun kelime, hece bölme doğru |
| bilgisayar hecele | deterministik | bilgisayar kelimesini doğru hecelemeli ve hece say | orta | deterministik | ✅ | Banka dışı uzun kelime (4 hece); 'lg' sessiz çifti bölünmesi ve çok he |
| televizyon kaç hece | deterministik | televizyon kelimesinin hece sayısını vermeli. | orta | deterministik | ✅ | Banka dışı uzun kelime; 'zy' sessiz çifti ve dört heceli yapı hece böl |
| kütüphaneyi hecele | deterministik | Hedef ek almış 'kütüphaneyi' olur; 'kütüphaneyi' k | tuzak | deterministik | ✅ | Ek + kaynaştırma harfi (kütüphane→kütüphaneyi) hedef olur; kök 'kütüph |

### harf sayımı (24)

| Soru | Beklenen katman | Beklenen cevap | Zorluk | Gerçek katman | Durum | Tuzak nedeni |
|------|-----------------|----------------|--------|---------------|-------|--------------|
| elma kaç harf | deterministik | 4 harf | kolay | deterministik | ✅ |  |
| kitap kaç harflidir? | deterministik | 5 harf | kolay | deterministik | ✅ |  |
| kalem kaç harf | deterministik | 5 harf | kolay | deterministik | ✅ |  |
| okul kaç harflidir? | deterministik | 4 harf | kolay | deterministik | ✅ |  |
| masa kaç harf | deterministik | 4 harf | kolay | deterministik | ✅ |  |
| kapı kaç harflidir? | deterministik | 4 harf | kolay | deterministik | ✅ |  |
| arı kaç harf | deterministik | 3 harf | kolay | deterministik | ✅ |  |
| çiçek kaç harflidir? | deterministik | 5 harf | kolay | deterministik | ✅ |  |
| bulut kaç harf | deterministik | 5 harf | kolay | deterministik | ✅ |  |
| tavuk kaç harflidir? | deterministik | 5 harf | kolay | deterministik | ✅ |  |
| kelebek kaç harf | deterministik | 7 harf | kolay | deterministik | ✅ |  |
| karpuz kaç harflidir? | deterministik | 6 harf | kolay | deterministik | ✅ |  |
| yağmur kaç harf | deterministik | 6 harf | orta | deterministik | ✅ |  |
| ışık kaç harflidir? | deterministik | 4 harf | orta | deterministik | ✅ |  |
| iğne kaç harf | deterministik | 4 harf | orta | deterministik | ✅ |  |
| kitapçı kaç harflidir? | deterministik | 7 harf | orta | deterministik | ✅ |  |
| gökyüzü kaç harf | deterministik | 7 harf | orta | deterministik | ✅ |  |
| ağaç kaç harflidir? | deterministik | 4 harf | orta | deterministik | ✅ |  |
| şemsiye kaç harf | deterministik | 7 harf | orta | deterministik | ✅ |  |
| uçak kaç harflidir? | deterministik | 4 harf | orta | deterministik | ✅ |  |
| balik kac harf | deterministik | 5 harf (balık) | tuzak | deterministik | ✅ | Aksan-duyarsiz eslesme: Turkce karaktersiz yazim dogru yakalanmali |
| isik kac harf | deterministik | 4 harf (ışık) | tuzak | deterministik | ✅ | Aksan-duyarsiz eslesme: Turkce karaktersiz yazim dogru yakalanmali |
| cicek kac harf | deterministik | 5 harf (çiçek) | tuzak | deterministik | ✅ | Aksan-duyarsiz eslesme: Turkce karaktersiz yazim dogru yakalanmali |
| ogretmen kac harf | deterministik | 8 harf (öğretmen) | tuzak | deterministik | ✅ | Aksan-duyarsiz eslesme: Turkce karaktersiz yazim dogru yakalanmali |

### sesli-sessiz (32)

| Soru | Beklenen katman | Beklenen cevap | Zorluk | Gerçek katman | Durum | Tuzak nedeni |
|------|-----------------|----------------|--------|---------------|-------|--------------|
| elma kaç sesli | deterministik | 2 sesli harf | kolay | deterministik | ✅ |  |
| kitap kaç sessiz | deterministik | 3 sessiz harf | kolay | deterministik | ✅ |  |
| kalem kaç sesli | deterministik | 2 sesli harf | kolay | deterministik | ✅ |  |
| okul kaç sessiz | deterministik | 2 sessiz harf | kolay | deterministik | ✅ |  |
| masa kaç sesli | deterministik | 2 sesli harf | kolay | deterministik | ✅ |  |
| kapı kaç sessiz | deterministik | 2 sessiz harf | kolay | deterministik | ✅ |  |
| arı kaç sesli | deterministik | 2 sesli harf | kolay | deterministik | ✅ |  |
| çiçek kaç sessiz | deterministik | 3 sessiz harf | kolay | deterministik | ✅ |  |
| bulut kaç sesli | deterministik | 2 sesli harf | kolay | deterministik | ✅ |  |
| tavuk kaç sessiz | deterministik | 3 sessiz harf | kolay | deterministik | ✅ |  |
| yağmur kaç sesli | deterministik | 2 sesli harf | orta | deterministik | ✅ |  |
| ışık kaç sessiz | deterministik | 2 sessiz harf | orta | deterministik | ✅ |  |
| iğne kaç sesli | deterministik | 2 sesli harf | orta | deterministik | ✅ |  |
| kitapçı kaç sessiz | deterministik | 4 sessiz harf | orta | deterministik | ✅ |  |
| gökyüzü kaç sesli | deterministik | 3 sesli harf | orta | deterministik | ✅ |  |
| ağaç kaç sessiz | deterministik | 2 sessiz harf | orta | deterministik | ✅ |  |
| kelebek kelimesinde kaç sesli harf var | deterministik | 3 sesli harf | orta | deterministik | ✅ |  |
| gökyüzü kelimesinde kaç sesli harf var | deterministik | 3 sesli harf | orta | deterministik | ✅ |  |
| a harfi sesli mi | deterministik | A → sesli (ünlü) | kolay | deterministik | ✅ |  |
| e sesli mi sessiz mi | deterministik | E → sesli (ünlü) | kolay | deterministik | ✅ |  |
| b ünsüz mü | deterministik | B → sessiz (ünsüz) | kolay | deterministik | ✅ |  |
| ğ harfi sesli mi | deterministik | Ğ → sessiz (ünsüz) | kolay | deterministik | ✅ |  |
| ı sesli mi sessiz mi | deterministik | I → sesli (ünlü) | kolay | deterministik | ✅ |  |
| i ünsüz mü | deterministik | İ → sesli (ünlü) | kolay | deterministik | ✅ |  |
| v harfi sesli mi | deterministik | V → sessiz (ünsüz) | kolay | deterministik | ✅ |  |
| z sesli mi sessiz mi | deterministik | Z → sessiz (ünsüz) | kolay | deterministik | ✅ |  |
| m ünsüz mü | deterministik | M → sessiz (ünsüz) | kolay | deterministik | ✅ |  |
| o harfi sesli mi | deterministik | O → sesli (ünlü) | kolay | deterministik | ✅ |  |
| ü sesli mi sessiz mi | deterministik | Ü → sesli (ünlü) | kolay | deterministik | ✅ |  |
| ş ünsüz mü | deterministik | Ş → sessiz (ünsüz) | kolay | deterministik | ✅ |  |
| r harfi sesli mi | deterministik | R → sessiz (ünsüz) | kolay | deterministik | ✅ |  |
| j sesli mi sessiz mi | deterministik | J → sessiz (ünsüz) | kolay | deterministik | ✅ |  |

### ilk-son harf (17)

| Soru | Beklenen katman | Beklenen cevap | Zorluk | Gerçek katman | Durum | Tuzak nedeni |
|------|-----------------|----------------|--------|---------------|-------|--------------|
| elma ilk harf | deterministik | İlk harf: E | kolay | deterministik | ✅ |  |
| kitap son harf | deterministik | Son harf: P | kolay | deterministik | ✅ |  |
| kalem ilk harf | deterministik | İlk harf: K | kolay | deterministik | ✅ |  |
| okul son harf | deterministik | Son harf: L | kolay | deterministik | ✅ |  |
| masa ilk harf | deterministik | İlk harf: M | kolay | deterministik | ✅ |  |
| kapı son harf | deterministik | Son harf: I | kolay | deterministik | ✅ |  |
| arı ilk harf | deterministik | İlk harf: A | kolay | deterministik | ✅ |  |
| çiçek son harf | deterministik | Son harf: K | kolay | deterministik | ✅ |  |
| bulut ilk harf | deterministik | İlk harf: B | kolay | deterministik | ✅ |  |
| tavuk son harf | deterministik | Son harf: K | kolay | deterministik | ✅ |  |
| yağmur ilk harf | deterministik | İlk harf: Y | orta | deterministik | ✅ |  |
| ışık son harf | deterministik | Son harf: K | orta | deterministik | ✅ |  |
| iğne ilk harf | deterministik | İlk harf: İ | orta | deterministik | ✅ |  |
| kitapçı son harf | deterministik | Son harf: I | orta | deterministik | ✅ |  |
| gökyüzü ilk harf | deterministik | İlk harf: G | orta | deterministik | ✅ |  |
| kalem kelimesinin ilk harfi nedir? | deterministik | İlk harf: K | kolay | deterministik | ✅ |  |
| deniz kelimesinin ilk harfi nedir? | deterministik | İlk harf: D | kolay | deterministik | ✅ |  |

### yanlış-kelime yakalama (26)

| Soru | Beklenen katman | Beklenen cevap | Zorluk | Gerçek katman | Durum | Tuzak nedeni |
|------|-----------------|----------------|--------|---------------|-------|--------------|
| kitap mı kalem mi daha uzun | model | İki kelimeyi karşılaştırıp hangisinin daha çok har | tuzak | konu-dışı yönlendirme | ⚠️ YANLIŞ-RED | Cümlede iki hedef kelime (kitap, kalem) var ama hiçbir deterministik t |
| ev ile okul hangisi çok harfli | model | Her iki kelimenin harf sayısını kıyaslayıp doğru o | tuzak | model | ✅ | 'kac harf' regexi 'harf'ten hemen önceki kelimeyi alır; burada 'çok' k |
| elma armut hangisi daha çok heceli | model | İki kelimenin hece sayısını karşılaştırıp doğru ol | tuzak | model | ✅ | 'kac hece' tetikleyicisi yok, sadece 'heceli' geçiyor ve regex 'heceli |
| top ve masa hangisinin harfi fazla | model | top ve masa kelimelerinin harf sayılarını kıyaslay | tuzak | model | ✅ | İki banka kelimesi (top, masa) var ama 'harfi fazla' ifadesi 'kac harf |
| köpek mi kedi mi kaç harfli | model | Soru iki kelimeyi karşılaştırma niyetinde; her iki | tuzak | model | ✅ | 'kac harf' regexi 'kaç harf'tan hemen önceki kelimeyi (kedi) yakalar v |
| kalem kitaptan kaç harf uzun | model | İki kelimenin harf sayısı farkını hesaplayıp doğru | tuzak | model | ✅ | 'kac harf' regexinden önce 'kitaptan' (kitap değil, ekli hâl) gelir; r |
| annemin adını hecele | model | İsmin verilmediğini nazikçe belirtip kullanıcıdan  | tuzak | deterministik | ⚠️ DET-FAZLA | 'hecele' regexi 'hecele'den önceki 'adını' kelimesini yakalar ve 'a-dı |
| benim adım kaç harf | model | Hangi ismin sorulduğu belli olmadığından kullanıcı | tuzak | deterministik | ⚠️ DET-FAZLA | 'kac harf' regexi 'kaç harf'tan önceki 'adım' kelimesini yakalayıp onu |
| bir kelimede kaç harf olur | model | Genel bir bilgi sorusu olarak ele alınmalı; kelime | tuzak | model | ✅ | 'bir' ve 'kelimede' WSTOP listesinde; 'kac harf' regexi her ikisini de |
| kelime kaç hecelidir | model | Belirli bir kelime verilmediği için hangi kelimeni | tuzak | deterministik | ⚠️ DET-FAZLA | 'kelime' WSTOP listesinde olduğundan hece regexi onu hedef alamaz ve n |
| bir kelime kaç hece içerir | model | Kelimelere göre hece sayısının değiştiğini açıklam | tuzak | deterministik | ⚠️ DET-FAZLA | 'bir' ve 'kelime' WSTOP; hece regexi hedef bulamaz ve modele düşer. Tu |
| masanın mı sandalyenin mi harfi çok | model | İki kelimenin (masa, sandalye) harf sayısını karşı | tuzak | model | ✅ | Kelimeler iyelik ekli ('masanın','sandalyenin') ve 'harfi çok' ifadesi |
| hecele bakalım okul kelimesini | deterministik | okul kelimesini doğru hecelere bölüp göstermeli (o | tuzak | deterministik | ✅ | İleri yönlü regex 'hecele su/bana X' kalıbını bekler; 'hecele bakalım  |
| defter mi silgi mi daha çok harfli acaba | model | defter ve silgi kelimelerinin harf sayısını kıyasl | tuzak | model | ✅ | İki kelime arasında karşılaştırma var; 'harfli' öncesi 'çok' kelimesi  |
| şu cümlede kaç harf var: Ali okula gitti | model | Tek kelime değil bir cümle sorulduğundan, cümleyi/ | tuzak | model | ✅ | 'cumle/cumlede' WSTOP listesinde ve regex hedef alamaz; ayrıca 'kaç ha |
| araba kelimesi mi otobüs kelimesi mi uzun | model | araba ve otobüs kelimelerini karşılaştırıp hangisi | tuzak | model | ✅ | 'kelimesi' tekrarları ve 'uzun' kelimesi var; deterministik tetikleyic |
| kuş kelimesinden önce kalem kelimesini hecele | deterministik | kullanıcının asıl istediği kalem kelimesini doğru  | tuzak | deterministik | ✅ | Cümlede iki kelime (kuş, kalem) ve 'hecele' var; regex 'hecele'den önc |
| deniz mi orman mı kaç heceli | model | Her iki kelimenin hece sayısını ayrı ayrı doğru ve | tuzak | model | ✅ | 'kac hece' regexi 'kaç heceli'den hemen önceki 'orman' kelimesini yaka |
| hangisi daha kısa kapı yoksa pencere | model | kapı ve pencere kelimelerinin uzunluğunu kıyaslayı | tuzak | konu-dışı yönlendirme | ⚠️ YANLIŞ-RED | İki hedef kelime var ama hiçbir 'kaç harf/hece/hecele' tetikleyicisi y |
| kitabın mı kalemin mi son harfi farklı | model | İki kelimenin son harflerini ayrı ayrı doğru söyle | tuzak | model | ✅ | 'son harf' regexi 'son harf'ten önceki 'kalemin' kelimesini yakalar ve |
| okul kelimesi kaç harf kitap kelimesi kaç harf | model | İki ayrı kelimenin (okul ve kitap) harf sayılarını | tuzak | deterministik | ⚠️ DET-FAZLA | İki ayrı 'kaç harf' sorusu tek mesajda; regex soldan ilk eşleşmeyi (ok |
| şemsiye mi şapka mı çok harf içeriyor | model | şemsiye ve şapka kelimelerinin harf sayılarını kıy | tuzak | model | ✅ | 'harf içeriyor' ifadesi 'kac harf' regexine uymaz; 'çok' kelimesi harf |
| adının ilk harfi ne benim | model | Hangi ad olduğu belirtilmediğinden kullanıcıdan is | tuzak | deterministik | ⚠️ DET-FAZLA | 'ilk harf' regexi 'ilk harf'ten önceki 'adının' kelimesini yakalayıp ' |
| bana bir kelime hecele | model | Hangi kelimenin hecelenmesi istendiği belli olmadı | tuzak | deterministik | ⚠️ DET-FAZLA | 'hecele' öncesi 'kelime' skip listesinde, 'bir' de WSTOP/skip kapsamın |
| limon portakaldan kaç hece fazla | model | limon ve portakal kelimelerinin hece sayısı farkın | tuzak | model | ✅ | 'kac hece' regexinden önce 'portakaldan' (ekli) gelir; regex onu yakal |
| sınıf mı sınav mı yazması zor, hangisi çok harfli | model | sınıf ve sınav kelimelerinin harf sayılarını kıyas | tuzak | model | ✅ | Cümlede iki benzer kelime (sınıf, sınav) ve araya giren 'yazması zor'  |

### imla (26)

| Soru | Beklenen katman | Beklenen cevap | Zorluk | Gerçek katman | Durum | Tuzak nedeni |
|------|-----------------|----------------|--------|---------------|-------|--------------|
| herkez mi herkes mi | deterministik | Yanlış form 'herkez' geçtiği için doğru yazımın 'h | kolay | deterministik | ✅ |  |
| yanlız mı yalnız mı doğru | deterministik | Yanlış form 'yanlız' geçtiği için doğrusunun 'yaln | kolay | deterministik | ✅ |  |
| yalnış mı yanlış mı | deterministik | Yanlış form 'yalnış' geçtiği için doğrusunun 'yanl | orta | deterministik | ✅ | yalnız:yanlız ve yanlış:yalnış çiftleri birbirine çok benzer; sistemin |
| birşey mi bir şey mi yazılır | deterministik | Yanlış form 'birşey' geçtiği için doğrusunun 'bir  | kolay | deterministik | ✅ |  |
| hergün mü her gün mü | deterministik | Yanlış form 'hergün' geçtiği için doğrusunun 'her  | kolay | deterministik | ✅ |  |
| çünki mi çünkü mü doğrusu | deterministik | Yanlış form 'çünki' geçtiği için doğrusunun 'çünkü | kolay | deterministik | ✅ |  |
| öğretmenim sağol dedim | deterministik | Cümlede yanlış form 'sağol' geçtiği için (niyet ar | orta | deterministik | ✅ | Soru değil günlük cümle; yine de yanlış yazım her geçtiğinde düzeltilm |
| şuan dışarıdayım | deterministik | Cümlede yanlış form 'şuan' geçtiği için doğrusunun | tuzak | deterministik | ✅ | Günlük cümle, yazım niyeti yok; ama YANLIS form 'şuan' her geçtiğinde  |
| şu an toplantı var | konu-dışı yönlendirme | DOGRU form 'şu an' ve yazım niyeti olmadığından dü | tuzak | konu-dışı yönlendirme | ✅ | Doğru form niyet olmadan günlük cümlede geçiyor; 'şu an' düzeltilmemel |
| şu an ne yapıyorsun | konu-dışı yönlendirme | Doğru form 'şu an', yazım niyeti yok, konu anahtar | tuzak | konu-dışı yönlendirme | ✅ | Doğru imla formu sohbet sorusu içinde; imla düzeltmesi tetiklenmemeli. |
| film nasıl çekilir | konu-dışı yönlendirme | 'film' bir imla çiftinin doğru formu olsa da yazım | tuzak | konu-dışı yönlendirme | ✅ | Doğru form 'film' geçiyor ama niyet sınırı: 'nasıl çekilir' yazım düze |
| makine nasıl çalışır | konu-dışı yönlendirme | 'makine' doğru form olsa da yazım niyeti yok; konu | tuzak | konu-dışı yönlendirme | ✅ | Doğru form + niyetsiz genel 'nasıl çalışır' sorusu imla düzeltmesini t |
| makine mi makina mı yazılır | deterministik | Yanlış form 'makina' geçtiği için doğrusunun 'maki | orta | deterministik | ✅ |  |
| bilgisayar programı açılmıyor | konu-dışı yönlendirme | Doğru form 'program' geçiyor ama yazım niyeti ve k | tuzak | konu-dışı yönlendirme | ✅ | Doğru imla formu günlük cümlede; 'bilgisayar' konu anahtarı değil, iml |
| proğram mı program mı doğru | deterministik | Yanlış form 'proğram' geçtiği için doğrusunun 'pro | orta | deterministik | ✅ |  |
| Ali de geldi | konu-dışı yönlendirme | Bağlaç 'de' günlük cümlede; yazım/kural niyeti yok | tuzak | konu-dışı yönlendirme | ✅ | de/da yalnızca yazım/kural niyetiyle eşleşir; günlük cümlede TETIKLENM |
| geldim ki kimse yok | konu-dışı yönlendirme | 'ki' günlük cümlede; yazım niyeti ve konu anahtarı | tuzak | konu-dışı yönlendirme | ✅ | ki bağlacı yalnızca yazım/kural niyetiyle eşleşir; düz cümlede tetikle |
| de da nasıl yazılır | deterministik | de/da kuralını verir: bağlaç 'de/da' ayrı, hâl eki | kolay | deterministik | ✅ |  |
| ev de mi evde mi yazılır | deterministik | de/da kuralını verir; 'yaz' niyeti ve 'de' hedef k | orta | deterministik | ✅ |  |
| hiç bir şey anlamadım | deterministik | Yanlış form 'hiç bir' geçtiği için doğrusunun 'hiç | tuzak | deterministik | ✅ | Günlük cümle gibi görünse de yanlış form 'hiç bir' her geçtiğinde düze |
| birkaç ayrı mı yazılır | deterministik | 'birkaç' doğru formu + 'ayrı' yazım niyeti olduğu  | orta | deterministik | ✅ | Doğru form ama 'ayrı' niyet kelimesi var; bu yüzden deterministik teti |
| herzaman geç kalıyor | deterministik | Yanlış form 'herzaman' geçtiği için doğrusunun 'he | orta | deterministik | ✅ |  |
| her zaman geç kalıyor | konu-dışı yönlendirme | DOGRU form 'her zaman' + yazım niyeti yok + konu a | tuzak | konu-dışı yönlendirme | ✅ | Bir önceki sorunun doğru-form ikizi: doğru yazıldığında niyet yoksa dü |
| hoşgeldin dedim ona | deterministik | Yanlış form 'hoşgeldin' geçtiği için doğrusunun 'h | orta | deterministik | ✅ |  |
| orjinal mı orijinal mi | deterministik | Yanlış form 'orjinal' geçtiği için doğrusunun 'ori | kolay | deterministik | ✅ |  |
| yada nasıl yazılır | deterministik | Yanlış form 'yada' geçtiği için doğrusunun 'ya da' | orta | deterministik | ✅ |  |

### noktalama (18)

| Soru | Beklenen katman | Beklenen cevap | Zorluk | Gerçek katman | Durum | Tuzak nedeni |
|------|-----------------|----------------|--------|---------------|-------|--------------|
| nokta nereye konur | deterministik | Nokta (.) cümlenin sonuna konur açıklaması; örnek  | kolay | deterministik | ✅ |  |
| virgul nereye konur | deterministik | Virgül (,) sıralanan kelimeleri ayırır açıklaması; | tuzak | deterministik | ✅ | Eksik Türkçe karakter (virgul). fold() ile 'virgül'→'virgul' eşleşmeli |
| soru isareti ne zaman kullanilir | deterministik | Soru işareti (?) soru cümlesinin sonuna konur açık | tuzak | deterministik | ✅ | Aksan-duyarsız: 'soru isareti' foldlanmadan da '/soru isaret/' regexin |
| ünlem işareti nerede kullanılır | deterministik | Ünlem (!) sevinç, heyecan, seslenme bildirir açıkl | kolay | deterministik | ✅ |  |
| noktalama işaretleri nelerdir | deterministik | Noktalama işaretleri listesi: nokta, virgül, soru  | tuzak | deterministik | ✅ | Metinde 'nokta' alt dizesi de var ama '!noktalama' guard'ı sayesinde t |
| noktalama nedir | deterministik | Noktalama işaretlerinin ne olduğu / listesi; tek b | tuzak | deterministik | ✅ | 'noktalama' içinde 'nokta' geçer; kod önce '/nokta/&&!/noktalama/' kon |
| iki nokta ne zaman konur | deterministik | İki nokta (:) açıklama/örnek sıralanacağında konur | tuzak | deterministik | ✅ | 'iki nokta' içinde 'nokta' var; FAQ 'iki nokta' anahtarı inline '/nokt |
| iki nokta üst üste neye yarar | deterministik | İki nokta (:) açıklama veya sıralama öncesi konur  | tuzak | deterministik | ✅ | Yine 'iki nokta'+'nokta' çakışması; FAQ 'iki nokta' anahtarı yakalamaz |
| kesme işareti nereye konur | deterministik | Kesme işareti (') özel isimlere gelen ekleri ayırı | orta | deterministik | ✅ |  |
| kesme isareti ne ise yarar | deterministik | Kesme işareti (') özel isim eklerini ayırır açıkla | tuzak | deterministik | ✅ | Aksan-duyarsız ('kesme isareti'); ayrıca 'kesme' inline regexte yok, y |
| ali'nin kalemi cümlesinde kesme işareti neden var | deterministik | Kesme işareti açıklaması: özel isme gelen ekleri a | tuzak | deterministik | ✅ | Cümlede gerçek kesme işareti (') var; localAnswer onu siliyor (Ali'nin |
| noktalı virgül nedir | deterministik | Noktalı virgül (;) açıklaması: virgülle ayrılmış g | tuzak | deterministik | ✅ | İçinde hem 'nokta' hem 'virgul' geçer; FAQ 'noktali virgul' anahtarı ö |
| cümlenin sonuna hangi işaret konur | deterministik | Cümle sonuna anlamına göre nokta, soru işareti vey | orta | deterministik | ✅ |  |
| öğretmenim bugün hava güzel cümlesinin sonuna ne koymalıyım | deterministik | Cümle sonu işareti açıklaması (nokta/soru/ünlem);  | tuzak | model | ⚠️ DET-KAÇIŞ | 'nokta/virgül' gibi anahtar kelime yok; FAQ kany 'sonuna hangi/sona ha |
| Ali de geldi cümlesinde virgül var mı | deterministik | Virgül (,) sıralanan kelimeleri ayırır genel açıkl | tuzak | model | ⚠️ DET-KAÇIŞ | 'virgül' kelimesi geçtiği için inline '/virgul/' tetiklenir ve genel v |
| nokta ile virgül arasındaki fark ne | deterministik | Hangi cevabın döndüğü kod sırasına bağlı: 'nokta'+ | tuzak | model | ⚠️ DET-KAÇIŞ | İki kavram sorulsa da kod tek cevap verir; '/nokta/&&!/noktalama/' ilk |
| tırnak işareti nasıl kullanılır | konu-dışı yönlendirme | Deterministik eşleşme yok; 'tırnak/işaret' TOPIC_W | tuzak | konu-dışı yönlendirme | ✅ | Çocuk gerçek bir noktalama işareti (tırnak) sorar ama ne FAQ'ta ne inl |
| parantez ne işe yarar | konu-dışı yönlendirme | Deterministik eşleşme yok; 'parantez' TOPIC_WORDS' | orta | konu-dışı yönlendirme | ✅ | Geçerli bir noktalama sorusu olmasına rağmen konu anahtarı içermediği  |

### büyük harf (10)

| Soru | Beklenen katman | Beklenen cevap | Zorluk | Gerçek katman | Durum | Tuzak nedeni |
|------|-----------------|----------------|--------|---------------|-------|--------------|
| büyük harf ne zaman kullanılır? | deterministik | Büyük harfin iki kullanım yerini açıklamalı: cümle | kolay | deterministik | ✅ | Düz, kalıba birebir uyan soru; tuzak yok. |
| Buyuk harf ne zaman yazilir | deterministik | Yine büyük harf kuralı dönmeli. fold() ile 'buyuk  | orta | deterministik | ✅ | Aksan-duyarsız: 'büyük'→'buyuk', 'yazılır'→'yazilir'. fold() sayesinde |
| büyük ve küçük harf arasındaki fark nedir | deterministik | Büyük/küçük harf farkını anlatan banka cevabı dönm | orta | deterministik | ✅ | 'büyük harf' tek parça geçmiyor; faqLookup'taki kany 'büyük ve küçük'/ |
| küçük harf ne demek | deterministik | FAQ 'büyük ve küçük harf' cevabı dönmeli (k:['harf | tuzak | deterministik | ✅ | İçinde 'büyük harf' YOK, sadece 'küçük harf' var. /buyuk harf/ kuralı  |
| büyükharf ne zaman kullanılır? | model | Konuyla ilgili olduğu için modele gider; modelin b | tuzak | model | ✅ | Bitişik 'büyükharf' → fold 'buyukharf'. /buyuk harf/ ve FAQ 'büyük har |
| özel isimler neden büyük harfle başlar | deterministik | İçinde 'büyük harf' geçtiği için /buyuk harf/ kura | orta | deterministik | ✅ | 'özel isim' FAQ'sine de benzer ama önce faqLookup denenir; 'özel isim' |
| a harfi büyük mü küçük mü | model | Konuyla ilgili (harf) olduğu için modele gider. De | tuzak | model | ✅ | Tek-harf regex'i sadece (sesli\|unlu\|sessiz\|unsuz) m[iu] kalıbını ya |
| cümlenin ilk harfi neden büyük yazılıyor | deterministik | İçinde 'büyük' + 'harf' birlikte 'büyük ... harf'  | tuzak | deterministik | ✅ | TUZAK: 'ilk harfi neden büyük' sırasında 'harf' ile 'büyük' bitişik DE |
| Ankarada büyük harfle mi yazılır | deterministik | İçinde 'büyük harf' (büyük harfle) geçtiği için /b | orta | deterministik | ✅ | 'büyük harfle' → fold 'buyuk harfle', /buyuk harf/ alt-dize olarak tut |
| gün ve ay isimleri büyük harfle mi başlar | deterministik | İçinde 'büyük harf' geçtiği için /buyuk harf/ gene | tuzak | deterministik | ✅ | Beklenen ideal cevap gün/ay özel kuralıdır (FAQ 1665 'gün'/'ay' k'leri |

### alfabe (10)

| Soru | Beklenen katman | Beklenen cevap | Zorluk | Gerçek katman | Durum | Tuzak nedeni |
|------|-----------------|----------------|--------|---------------|-------|--------------|
| alfabede kaç harf var? | deterministik | 29 harf (8 sesli, 21 sessiz) cevabı. /alfabe/ + 'k | kolay | deterministik | ✅ | Kalıba birebir uyan düz soru; tuzak yok. |
| alfabede kac tane harf var | deterministik | 29 harf cevabı dönmeli. fold ile 'kac tane' eşleşi | orta | deterministik | ✅ | Aksan-duyarsız ('kaç'→'kac') ve 'kac tane' varyantı; eksik Türkçe kara |
| Türk alfabesi nasıl sıralanır | deterministik | Alfabe sırası (a b c ç ...) cevabı; FAQ 'alfabe sı | orta | deterministik | ✅ | 'kaç harf' yok, sayım kuralı tutmaz; faqLookup'taki 'sıra' anahtarı 's |
| alfabenin ilk harfi nedir | model | Modele gider (A harfi cevabı modelden beklenir). D | tuzak | model | ✅ | wq() yakaladığı kelime 'alfabenin' → /^alfabe/ ile REDDEDİLİR (null).  |
| kaç harf var | model | Modele gider. Deterministik alfabe kuralı yalnızca | tuzak | model | ✅ | Yorumda açıkça belirtilmiş: çıplak 'kaç harf' (alfabe yok) modele gits |
| alfabede kac harf var | deterministik | 29 harf cevabı. Türkçe karaktersiz yazımda da /alf | tuzak | deterministik | ✅ | Tamamen aksansız çocuk yazımı ('alfabede kac harf'). fold() her iki an |
| ğ ile başlayan kelime var mı | deterministik | Hiçbir Türkçe kelime ğ ile başlamaz cevabı; FAQ 'ğ | orta | deterministik | ✅ | faqLookup w:'ğ' TAM token ister; 'ğ' ayrı kelime olarak geçer ('ğ ile  |
| g ile baslayan kelime olur mu | model | Modele gider. Kullanıcı 'ğ' yerine 'g' (ve aksansı | tuzak | model | ✅ | TUZAK: faqLookup w:'ğ' eşleşmesi Türkçe-korumalı normT üzerinden yapıl |
| alfabe ne demek | model | Modele gider. 'kaç harf/tane/say' veya 'sıra' geçm | tuzak | model | ✅ | 'alfabe' geçiyor ama tek başına yetmez: alfabe kuralı 'kac harf\|kac t |
| alfabede sesli harfler kaç tane | deterministik | Sesli harf listesi + 8 tane cevabı dönmeli (wantsS | tuzak | deterministik | ✅ | 'alfabe' + 'kac tane' var; sezgi 'alfabede 29 harf' der. Ama localAnsw |

### FAQ-kural (25)

| Soru | Beklenen katman | Beklenen cevap | Zorluk | Gerçek katman | Durum | Tuzak nedeni |
|------|-----------------|----------------|--------|---------------|-------|--------------|
| hece nedir? | deterministik | Hece kavramının tanımını verir: ağızdan bir defada | kolay | deterministik | ✅ |  |
| kelime nedir | deterministik | Kelime (sözcük) tanımı: anlamı olan ses/harf toplu | kolay | deterministik | ✅ |  |
| harf nedir? | deterministik | Harf tanımı: sesleri gösteren işaretler; alfabede  | kolay | deterministik | ✅ |  |
| cümle nedir | deterministik | Cümle tanımı: bir duygu/düşünceyi tam anlatan keli | kolay | deterministik | ✅ |  |
| özel isim nedir hocam | deterministik | Özel isim tanımı: tek bir varlığa verilen ad (Ali, | orta | deterministik | ✅ |  |
| i ile ı farkı nedir | deterministik | Noktalı i ile noktasız ı'nın ayrı harfler olduğu;  | orta | deterministik | ✅ |  |
| hece nasıl bölünür? | deterministik | Hece bölme kuralı: her hecede bir sesli; iki sesli | kolay | deterministik | ✅ |  |
| nasıl daha iyi okurum | deterministik | Okuma tavsiyeleri: her gün biraz oku, kelimeleri b | kolay | deterministik | ✅ |  |
| de da nasıl yazılır? | deterministik | Bağlaç de/da ayrı yazılır (Ali de geldi), hâl eki  | orta | deterministik | ✅ |  |
| ki bağlacı ayrı mı yazılır | deterministik | Bağlaç ki ayrı yazılır (Duydum ki gelmişsin) kural | orta | deterministik | ✅ |  |
| mi soru eki nasıl yazılır | deterministik | Soru eki mı/mi/mu/mü'nün her zaman ayrı yazıldığı  | orta | deterministik | ✅ |  |
| hece ne demek | model | Hece kavramını çocuğa uygun, kısa ve doğru biçimde | tuzak | deterministik | ⚠️ DET-FAZLA | 'hece nedir' bankada k:['hece nedir'] ile sabittir; 'ne demek' varyant |
| cümle ne demek? | model | Cümle kavramını kısa ve doğru açıklamalı. Konu içi | tuzak | model | ✅ | 'cümle nedir' bankada k:['cümle nedir'] ile sabittir; 'ne demek' varya |
| sözcük ne demek | deterministik | Kelime (sözcük) tanımını döndürür. Banka kany'sind | tuzak | deterministik | ✅ | 'kelime' eş anlamlısı 'sözcük' + 'ne demek' varyantı bilerek eklenmiş; |
| harf ne demek | deterministik | Harf tanımını döndürür. Banka kany'sinde 'harf ne  | orta | deterministik | ✅ | 'ne demek' varyantı harf'te var (hece/cümle'de yok); aynı eki kullanan |
| sözcük nedir acaba | deterministik | Kelime (sözcük) tanımını döndürür. 'acaba' gibi ek | orta | deterministik | ✅ | Cümleye serbest kelime eklemenin alt-dize tabanlı kany eşleşmesini boz |
| i ve ı aynı harf mi | model | i ile ı'nın ayrı harfler olduğunu konu içi biçimde | tuzak | model | ✅ | i/ı bankası kany'si 'ile/fark/noktalı/noktasız' arar; 've aynı harf mi |
| sen de gel hadi | konu-dışı yönlendirme | Konu dışı yönlendirme mesajı verilmeli. | tuzak | konu-dışı yönlendirme | ✅ | Günlük konuşmada 'de' bağlacı; yazım niyeti ve TOPIC kelimesi yok. de/ |
| duydum ki gelmişsin | konu-dışı yönlendirme | Konu dışı yönlendirme mesajı verilmeli (ki günlük  | tuzak | konu-dışı yönlendirme | ✅ | 'ki' tam kelime geçer ama yazım/bağlaç niyeti (yaz/ayrı/nasıl/bağlaç)  |
| geldin mi | konu-dışı yönlendirme | Konu dışı yönlendirme mesajı verilmeli (mi soru ek | tuzak | konu-dışı yönlendirme | ✅ | 'mi' tam kelime geçer ama yazım/soru-eki niyeti (yaz/ayrı/soru/ek) ve  |
| mı eki nereye gelir | konu-dışı yönlendirme | Konu dışı yönlendirme mesajı verilmeli (beklenmedi | tuzak | konu-dışı yönlendirme | ✅ | Hedef kelime eşleşmesi (w:'mi') Türkçe-korumalı normT üzerinde yapılır |
| heceyi nasıl ayırırım | deterministik | Hece bölme kuralını döndürür; 'hece' + 'nasıl/ayır | orta | deterministik | ✅ | 'hece nedir' eşleşmesinden farklı olarak bu, 'hece nasıl bölünür' bank |
| büyük ve küçük harf farkı nedir | deterministik | Büyük/küçük harf açıklaması: cümle büyük harfle ba | orta | deterministik | ✅ | 'harf' (k) + 'büyük ve küçük' (kany) eşleşir. 'fark/nedir' eklenmesi e |
| daha hızlı nasıl okurum | deterministik | Okuma geliştirme tavsiyelerini döndürür; 'oku' (k) | orta | deterministik | ✅ | 'nasıl daha iyi okurum' bankasının kany'sinde 'hızlı' ve 'nasıl' bulun |
| de ayrı mı bitişik mi yazılır | deterministik | Bağlaç de/da ayrı, hâl eki -de/-da bitişik kuralın | tuzak | deterministik | ✅ | Günlük 'Ali de geldi' ile karşıtlık: burada açık yazım niyeti (ayrı/bi |

### konu-dışı (30)

| Soru | Beklenen katman | Beklenen cevap | Zorluk | Gerçek katman | Durum | Tuzak nedeni |
|------|-----------------|----------------|--------|---------------|-------|--------------|
| iki kere iki kaç eder? | konu-dışı yönlendirme | Matematik sorusu; deterministik boş döner, mesajda | kolay | konu-dışı yönlendirme | ✅ | Net konu dışı (matematik), tuzak değil. |
| hangi takım şampiyon oldu? | konu-dışı yönlendirme | Spor sorusu; TOPIC anahtarı içermez, konu-dışı yön | kolay | konu-dışı yönlendirme | ✅ | Net konu dışı (spor), tuzak değil. |
| yarın yağmur yağacak mı? | konu-dışı yönlendirme | Hava durumu sorusu; TOPIC anahtarı yok, yönlendirm | kolay | konu-dışı yönlendirme | ✅ | Net konu dışı (hava durumu), tuzak değil. |
| penguenler nerede yaşar? | konu-dışı yönlendirme | Hayvan bilgisi sorusu; TOPIC anahtarı yok, yönlend | kolay | konu-dışı yönlendirme | ✅ | Net konu dışı (hayvan bilgisi), tuzak değil. |
| dünyanın en uzun nehri hangisi? | konu-dışı yönlendirme | Coğrafya sorusu; TOPIC anahtarı yok, yönlendirme m | kolay | konu-dışı yönlendirme | ✅ | Net konu dışı (coğrafya), tuzak değil. |
| saklambaç nasıl oynanır? | konu-dışı yönlendirme | Oyun sorusu; TOPIC anahtarı yok, yönlendirme mesaj | kolay | konu-dışı yönlendirme | ✅ | Net konu dışı (oyun), tuzak değil. |
| makarna nasıl pişirilir | konu-dışı yönlendirme | Yemek sorusu; TOPIC anahtarı yok, yönlendirme mesa | kolay | konu-dışı yönlendirme | ✅ | Net konu dışı (yemek), tuzak değil. |
| ankara mı izmir mi daha büyük? | konu-dışı yönlendirme | Coğrafya sorusu; TOPIC anahtarı yok, yönlendirme m | kolay | konu-dışı yönlendirme | ✅ | Net konu dışı (coğrafya), tuzak değil. |
| arılar balı nasıl yapar? | konu-dışı yönlendirme | Bilim/hayvan sorusu; TOPIC anahtarı yok, yönlendir | kolay | konu-dışı yönlendirme | ✅ | Net konu dışı (hayvan bilgisi), tuzak değil. |
| dünya neden döner? | konu-dışı yönlendirme | Bilim sorusu; TOPIC anahtarı yok, yönlendirme mesa | kolay | konu-dışı yönlendirme | ✅ | Net konu dışı (bilim), tuzak değil. |
| kediler neden mırlar | konu-dışı yönlendirme | Hayvan bilgisi sorusu; TOPIC anahtarı yok, yönlend | kolay | konu-dışı yönlendirme | ✅ | Net konu dışı (hayvan bilgisi), tuzak değil. |
| çıkarma işlemi çok zor geliyor, anlatır mısın? | konu-dışı yönlendirme | Matematik sorusu; TOPIC anahtarı yok, yönlendirme  | orta | konu-dışı yönlendirme | ✅ | 'çıkarma/işlem' okuma-yazma gibi okul terimi çağrıştırır ama hiçbir TO |
| uzayda neden yer çekimi yok? | konu-dışı yönlendirme | Bilim sorusu; TOPIC anahtarı yok, yönlendirme mesa | kolay | konu-dışı yönlendirme | ✅ | Net konu dışı (bilim), tuzak değil. |
| deniz neden tuzludur? | konu-dışı yönlendirme | Bilim sorusu; TOPIC anahtarı yok, yönlendirme mesa | kolay | konu-dışı yönlendirme | ✅ | Net konu dışı (bilim), tuzak değil. |
| yüzme öğrenmek istiyorum | konu-dışı yönlendirme | Spor/etkinlik isteği; 'öğrenmek' içinde TOPIC alt- | orta | konu-dışı yönlendirme | ✅ | 'öğrenmek' okuma-yazma öğrenimini çağrıştırır ama TOPIC anahtarı içerm |
| timsah mı köpekbalığı mı daha güçlü? | konu-dışı yönlendirme | Hayvan bilgisi sorusu; TOPIC anahtarı yok, yönlend | kolay | konu-dışı yönlendirme | ✅ | Net konu dışı (hayvan bilgisi), tuzak değil. |
| futbol topu kaç parçadan oluşur? | konu-dışı yönlendirme | Spor sorusu; 'kaç' var ama hedef bir kelime + hece | tuzak | konu-dışı yönlendirme | ✅ | 'kaç ... oluşur' deterministik sayım kalıbına benzer ama hedef kelime  |
| gezegenleri sırayla sayar mısın? | konu-dışı yönlendirme | Bilim/coğrafya sorusu; 'sırayla/sayar' determinist | tuzak | konu-dışı yönlendirme | ✅ | 'sırayla say' sayım/sıralama kalıbını çağrıştırır ve 'sıra' kelimesi ' |
| bana dokunma! | konu-dışı yönlendirme | İçerik tamamen konu dışı; ideal davranış konu-dışı | tuzak | model | ⚠️ SIZINTI | TOPIC alt-dize sızıntısı: 'oku' (d-oku-nma). |
| yazılım mühendisi ne iş yapar? | konu-dışı yönlendirme | Meslek sorusu, konu dışı; ideal davranış yönlendir | tuzak | model | ⚠️ SIZINTI | TOPIC alt-dize sızıntısı: 'yaz' (yaz-ılım). |
| yeni yazıcı aldık ama çalışmıyor | konu-dışı yönlendirme | Cihaz/teknik şikayet, konu dışı; ideal davranış yö | tuzak | model | ⚠️ SIZINTI | TOPIC alt-dize sızıntısı: 'yaz' (yaz-ıcı). |
| abimin ses tonu çok kalın | konu-dışı yönlendirme | Günlük gözlem, konu dışı; ideal davranış yönlendir | tuzak | model | ⚠️ SIZINTI | TOPIC alt-dize sızıntısı: 'ses' (ses tonu — harf sesi değil). |
| gece her yer sessizlik içindeydi | konu-dışı yönlendirme | Betimleme cümlesi, konu dışı; ideal davranış yönle | tuzak | model | ⚠️ SIZINTI | TOPIC alt-dize sızıntısı: 'ses' (ses-sizlik). |
| Metin dayım bize hediye getirdi | konu-dışı yönlendirme | Aile/günlük cümle, konu dışı; ideal davranış yönle | tuzak | model | ⚠️ SIZINTI | TOPIC alt-dize sızıntısı: 'metin' (özel isim Metin, paragraf metni değ |
| basketbolda nokta atışı yaptım | konu-dışı yönlendirme | Spor cümlesi, konu dışı; ideal davranış yönlendirm | tuzak | model | ⚠️ SIZINTI | TOPIC alt-dize sızıntısı: 'nokta' (nokta atışı — noktalama işareti değ |
| yarın sınavda yazıyoruz, çok heyecanlıyım | konu-dışı yönlendirme | Genel okul-günlük cümlesi, belirli bir okuma-yazma | tuzak | model | ⚠️ SIZINTI | TOPIC alt-dize sızıntısı: 'yaz' (yaz-ıyoruz). |
| yaz gelince denize gireceğiz | konu-dışı yönlendirme | Mevsim/tatil cümlesi, konu dışı; ideal davranış yö | tuzak | model | ⚠️ SIZINTI | TOPIC alt-dize sızıntısı: 'yaz' (mevsim 'yaz', yazmak fiili değil). |
| midemde garip bir vurgu hissettim | konu-dışı yönlendirme | Sağlık/duygu cümlesi, konu dışı; ideal davranış yö | tuzak | model | ⚠️ SIZINTI | TOPIC alt-dize sızıntısı: 'vurgu' (hece vurgusu değil). |
| babam yazıhanede çalışıyor | konu-dışı yönlendirme | Aile/meslek cümlesi, konu dışı; ideal davranış yön | tuzak | model | ⚠️ SIZINTI | TOPIC alt-dize sızıntısı: 'yaz' (yaz-ıhane). |
| bu yaz çok sıcak olacak galiba | konu-dışı yönlendirme | Hava/mevsim cümlesi, konu dışı; ideal davranış yön | tuzak | model | ⚠️ SIZINTI | TOPIC alt-dize sızıntısı: 'yaz' (mevsim 'yaz'). |

### sınır/aykırı girdiler (17)

| Soru | Beklenen katman | Beklenen cevap | Zorluk | Gerçek katman | Durum | Tuzak nedeni |
|------|-----------------|----------------|--------|---------------|-------|--------------|
| a | konu-dışı yönlendirme | Tek başına bir harf bir soru içermez; deterministi | tuzak | konu-dışı yönlendirme | ✅ | Tek harf konuyla ilgili sanılabilir ama tek başına yazılınca ne determ |
| o sesli mi | deterministik | Tek harf sınıflandırma kalıbı tetiklenir; 'o' harf | orta | deterministik | ✅ | Tek harf normalde sınırda ama burada 'harfi sesli mi' kalıbına uyduğu  |
| b hecele | deterministik | Hedef kelime tek harf olduğu için heceleme regexi  | tuzak | deterministik | ✅ | 'hecele' niyeti var ama hedef 'b' tek harf; {2,} sınırına takılır. Spe |
| kütüphanecilik kaç hece | deterministik | Çok uzun da olsa 'kaç hece' kalıbı tetiklenir; hec | orta | deterministik | ✅ | Uzunluk üst sınırı yok; algoritmanın uzun kelimede de çalışması ve mod |
| 12345 | konu-dışı yönlendirme | Sadece rakam; localAnswer hiçbir kalıba uymaz, içi | kolay | konu-dışı yönlendirme | ✅ | Rakam dizisi sayma çağrışımı yapsa da deterministik kelime regexleri h |
| 12345 kaç harf | konu-dışı yönlendirme | 'kaç harf' geçse de hedef token rakamdır; 'kac har | tuzak | model | ⚠️ SIZINTI | Deterministik yakalayamaz (rakam hedef) ama mesajda 'harf' alt-dizesi  |
| !!!??? | konu-dışı yönlendirme | Sadece noktalama işaretleri; hiçbir deterministik  | orta | konu-dışı yönlendirme | ✅ | Soru/ünlem işareti 'noktalama' konusunu çağrıştırır ama metinde 'nokta |
| asdfgh | konu-dışı yönlendirme | Anlamsız klavye dizisi; localAnswer kalıplarına uy | kolay | konu-dışı yönlendirme | ✅ | Harflerden oluşması 'kelime/harf' işlemi sanılabilir ama tek başına bi |
| qwerty | konu-dışı yönlendirme | Anlamsız klavye dizisi, niyet kelimesi yok, TOPIC  | orta | konu-dışı yönlendirme | ✅ | İngilizce klavye dizisi; içinde 'yaz','oku','ses' gibi hiçbir TOPIC al |
| ne | konu-dışı yönlendirme | İki harfli ama bir niyet/işlem kalıbı içermez; 'ne | orta | konu-dışı yönlendirme | ✅ | Soru kelimesi gibi durur ama tek başına; deterministik kalıplara uymaz |
| sa | konu-dışı yönlendirme | İki harfli anlamsız token; deterministik kalıba uy | tuzak | konu-dışı yönlendirme | ✅ | 'sa' kısa olduğu için 'ses' alt-dizesi sanılabilir ama 'ses' s-e-s'tir |
| Bugün hava cok guzel ve disarida yagmur yagiyor sanirim | konu-dışı yönlendirme | Uzun, doğal ama okuma-yazma konusuyla ilgisiz cüml | tuzak | konu-dışı yönlendirme | ✅ | Uzun ve akıcı olması modele gitme beklentisi yaratır; ama fold edilse  |
| bir sey yazsana bana | model | Deterministik kalıba uymaz; ancak 'yazsana' içinde | tuzak | model | ✅ | Aslında okuma-yazma sorusu değil ama 'yazsana' kelimesi 'yaz' alt-dize |
| 😀😀😀 | konu-dışı yönlendirme | Sadece emoji; trim sonrası boş değil ama hiçbir ha | orta | konu-dışı yönlendirme | ✅ | Emoji boş girdi gibi davranır sanılabilir ama trim onu silmez; yine de |
| okyanus kaç harf | deterministik | 'okyanus kac harf' kelime sayım kalıbına uyar; oky | tuzak | deterministik | ✅ | 'okyanus' içinde 'oku' yok gibi görünür (o-k-y) ama bu örnekte determi |
| asdf hecele | deterministik | 'asdf' geçerli bir kelime olmasa da [a-z]{2,} ve ' | tuzak | deterministik | ✅ | Anlamsız kelime girilse de deterministik heceleme onu işler; sesli har |
| KÜTÜPHANECİLİK KAÇ HECE | deterministik | Tamamı büyük ve Türkçe karakterli olsa da trLower+ | orta | deterministik | ✅ | Hem büyük harf, hem uzunluk, hem İ/Ü/Ç gibi karakterlerin üst üste bin |
