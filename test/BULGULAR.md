# Bulgular Raporu — Düzeltme Sonrası

> 287 test sorusu, sistemin gerçek mantığının birebir portundan (`test/sim.py`)
> geçirildi. Sonuç: **261/287 OK**. Aşağıda (1) güncel kodun zaten karşıladıkları,
> (2) bu turda düzeltilenler, (3) bilerek bırakılan (kabul edilebilir) durumlar.
>
> Gerçek JS, asıl `faq.js` ile Node'da ayrıca koşturulup doğrulandı.

---

## ✅ Bu turda düzeltilenler

### 1. Yanlış-kelime yakalama — karşılaştırma sorularında
Önceden `ev ile okul hangisi çok harfli` → "okul 4 harf"; `köpek mi kedi mi kaç harfli`
→ "**mi** 2 harf" gibi yanlış tek-kelime cevapları dönüyordu.

**Çözüm** (`localAnswer`, `okuma-yazma-asistani.html`): karşılaştırma sezici `cmp`.
"hangisi" veya iki soru eki **+ sayım/uzunluk bağlamı** (kaç/harf/hece/uzun/kısa…),
ya da "daha çok/uzun…", ya da "kaç harf/hece fazla" varsa deterministik sayım/heceleme/
banka eşleşmesi **atlanır**, soru modele gider.

> İncelik: "hangi/iki soru eki" yalnızca sayım bağlamıyla karşılaştırma sayılır;
> böylece imla düzeltmeleri (`herkez mi herkes mi`, `proğram mı program mı`) — ki bunların
> da iki soru eki vardır ama sayım bağlamı yoktur — **engellenmez**.

| Soru | Önce | Sonra |
|------|------|-------|
| `köpek mi kedi mi kaç harfli` | "mi 2 harf" | → model |
| `ev ile okul hangisi çok harfli` | "okul 4 harf" | → model |
| `elma armut hangisi daha çok heceli` | "armut 2 hece" | → model |
| `deniz mi orman mı kaç heceli` | "deniz 2 hece" | → model |
| `kalem kitaptan kaç harf uzun` | "kitaptan 8 harf" | → model |

### 2. Soru eki "mı/mi" hedef kelime sayılması
`köpek mi kedi mi kaç harfli` → "**mi** kelimesinde 2 harf" hatasının ikinci kökü.
**Çözüm:** `mı/mi/mu/mü` artık `WSTOP`'ta — sayım regexlerinde hedef kelime olamaz.

### 3. Soru eki FAQ'i alakasız soruları yakalaması
`timsah mı köpekbalığı mı daha güçlü?` → "Soru eki ayrı yazılır" dönüyordu
("köp**ek**" → kısa "ek" niyeti). **Çözüm** (`gen_faq.py`): "mi soru eki" kany'si
`["yaz","ayrı","soru eki","soru ek"]` (kısa "ek" çıkarıldı). Ayrıca `cmp` de yakalıyor.

### 4. Noktalama'nın niyet olmadan tetiklenmesi
`basketbolda nokta atışı yaptım` → nokta kuralı; `kesme şeker` → kesme işareti kuralı
riski. **Çözüm:**
- `gen_faq.py`: nokta/virgül/ünlem/kesme FAQ kayıtlarına niyet (`NI` = nereye, ne zaman,
  nasıl, konur, kullanıl, işaret…) eklendi.
- `localAnswer`: noktalama fallback'i de aynı niyet kapısına (`pi`) bağlandı.

| Soru | Önce | Sonra |
|------|------|-------|
| `basketbolda nokta atışı yaptım` | Nokta kuralı (yanlış) | → model |
| `nokta nereye konur` | Nokta kuralı | Nokta kuralı (korundu) |
| `virgül ne işe yarar` | Virgül kuralı | Virgül kuralı (korundu) |

---

## 🟢 Güncel kodun ZATEN karşıladıkları (son commit'lerde çözülmüş)
İlk taramada bulgu sanılan ama güncel kodda zaten doğru çalışanlar:

- **Aksan-duyarsızlık:** `isik kac harf` → "4 harf" (foldlu `tf` üzerinde eşleşme).
- **`b ünsüz mü`:** tek-harf regexi `m[iu]` → "B sessiz harftir".
- **g/ğ ayrımı:** `g ile başlayan kelime` artık "ğ başlamaz" demiyor (FAQ `w` Türkçe-korumalı `normT`).
- **Alfabe fallback:** `şu cümlede kaç harf var`, `12345 kaç harf` → artık "29" demiyor
  (`/alfabe/` + sayım şartı).

---

## ⚪ Bilerek bırakılanlar (kabul edilebilir / tasarım gereği)

- **Konu-dışı sızıntı (alt-dize):** `yazılım`, `yazıcı`, `ses tonu`, `dokunma`('oku'),
  `Metin amca` → modele gidiyor. `onTopic`'i kelime-sınırlı yapmak `yazma`, `okuma`,
  `yazılır` gibi **çekimli geçerli** biçimleri de keserdi. Bunlar modele gidince sistem
  promptunun kapsam kısıtı ("konu dışıysa yalnızca yönlendir") devreye girer — yanlış
  bilgi verilmez, sadece bir API çağrısı harcanır. Sert bug değil.
- **Karşılaştırma → konu-dışı:** `kitap mı kalem mi daha uzun` artık (doğru biçimde)
  tek kelimeye cevap vermiyor; konu kelimesi içermediği için konu-dışı yönlendirmeye
  düşüyor. Yanlış cevaptan iyidir.
- **Çekimli/zamir kelimeler:** `benim adım kaç harf` → "adım 4 harf". Sistem çocuğun
  ismini bilemez; literal kelimeyi işlemesi savunulabilir.
- **`hece ne demek`** → heceleme kuralı (tanım değil). `hece nedir` tanım verir. Küçük
  tutarsızlık, ikisi de yanlış değil.

---

## Sayısal özet

| | Önce (eski port) | Doğru port (düzeltme öncesi) | Düzeltme sonrası |
|---|---|---|---|
| OK | 240 | 254 | **261** |
| Ciddi bulgu | 17 | 15 | (kalan ciddi sınıfı: 2 karşılaştırma→konu-dışı, geri kalanı yumuşak sızıntı) |
| Yanlış-kelime (DET-FAZLA) | 24 | 17 | **8** (hepsi kabul edilebilir) |

### Yeniden üretmek için
```
python gen_faq.py        # faq.js'i yeniden üretir (noktalama niyet kapısı dahil)
python test/sim.py       # simülatör kendi-testi (16/16)
python test/build.py     # 287 soruyu geçirir → test-sorulari.md + .json + bu özet
```
