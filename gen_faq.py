# -*- coding: utf-8 -*-
"""
gen_faq.py — okuma-yazma-asistani icin TDK soru bankasi (faq.js) uretir.
Iki kaynak: (1) kelime listesinden programatik uretim (heceleme algoritmasi ile,
yapisi geregi dogru), (2) elle kurgulanmis kural/imla sorulari.
Cikti: faq.js  ->  window.OW_FAQ = [ {q, a, w, k?, kany?}, ... ]
  w     : hedef kelime (TAM kelime eslesir)
  k     : tum bu alt dizeler soruda gecmeli (intent)
  kany  : bunlardan en az biri gecmeli (imla niyeti)
Calistir: python gen_faq.py
"""
import json

VOWELS = set("aeıioöuüAEIİOÖUÜ")
SESLI = list("aeıioöuü")
SESSIZ = list("bcçdfgğhjklmnprsştvyz")  # 21 (j dahil)

def hece_bol(w):
    w = w.strip()
    vi = [i for i, ch in enumerate(w) if ch in VOWELS]
    if len(vi) <= 1:
        return [w]
    cuts = []
    for k in range(len(vi) - 1):
        a, b = vi[k], vi[k + 1]
        between = b - a - 1
        cuts.append(a + 1 if between == 0 else b - 1)
    parts, start = [], 0
    for c in cuts:
        parts.append(w[start:c]); start = c
    parts.append(w[start:])
    return parts

def tr_upper(ch):
    return {'i': 'İ', 'ı': 'I'}.get(ch, ch.upper())

def n_sesli(w):  return sum(1 for ch in w if ch in SESLI)
def n_sessiz(w): return sum(1 for ch in w if ch in SESSIZ)

# ------------------------------------------------------------------ KELIME LISTESI
KELIMELER = """
arı top masa kitap okul elma kapı kalem çiçek bulut tavuk bebek ayak yılan çanta
sepet limon karpuz kuş balık kedi köpek aslan kaplan fil tilki ayı kurt geyik maymun
zürafa fare horoz ördek kaz inek koyun keçi at eşek deve baykuş kelebek karınca sinek
örümcek solucan yengeç ahtapot köstebek sincap kirpi
ev oda kapı pencere duvar tavan çatı bahçe merdiven asansör mutfak banyo salon yatak
yastık yorgan halı perde lamba sandalye dolap masa ayna saat tabak kaşık çatal bardak
şişe tencere tava bıçak havlu sabun fırça tarak makas iğne düğme ip kova
ekmek peynir zeytin reçel bal süt yumurta tereyağı çorba pilav makarna köfte tavuk
salata domates salatalık biber patlıcan kabak havuç patates soğan sarımsak maydanoz
nane marul ıspanak elma armut muz çilek kiraz üzüm portakal mandalina nar incir kayısı
şeftali erik dut ceviz fındık fıstık badem
güneş ay yıldız gökyüzü deniz göl ırmak dere dağ tepe orman ağaç yaprak çimen taş kum
toprak yağmur kar rüzgar şimşek gökkuşağı bulut sis çiy buz ateş duman
anne baba abla ağabey kardeş dede nine teyze hala amca dayı kuzen torun bebek çocuk
öğretmen doktor polis asker şoför aşçı terzi marangoz çiftçi bakkal manav berber
okul sınıf öğrenci ders tahta silgi defter cetvel boya kitap çanta sıra zil teneffüs
baş saç göz kaş kulak burun ağız dil diş dudak yanak çene boyun omuz kol el parmak
tırnak göğüs karın sırt bacak diz ayak topuk kalp
kırmızı mavi sarı yeşil mor turuncu pembe siyah beyaz gri kahverengi lacivert
araba otobüs tren uçak gemi bisiklet motor kamyon vapur metro taksi
bir iki üç dört beş altı yedi sekiz dokuz on yüz bin
pazartesi salı çarşamba perşembe cuma cumartesi pazar
kış ilkbahar yaz sonbahar sabah öğle akşam gece
mutlu üzgün kızgın korkak cesur tembel çalışkan temiz kirli güzel çirkin küçük büyük
uzun kısa kalın ince hızlı yavaş sıcak soğuk yumuşak sert tatlı acı ekşi
koşmak yürümek atlamak gülmek ağlamak uyumak yemek içmek okumak yazmak çizmek bakmak
""".split()

# tekrarlari at, sirayi koru
seen = set(); kelimeler = []
for w in KELIMELER:
    w = w.strip().lower()
    if w and w not in seen:
        seen.add(w); kelimeler.append(w)

faq = []

def add(q, a, w=None, k=None, kany=None):
    e = {"q": q, "a": a}
    if w: e["w"] = w
    if k: e["k"] = k
    if kany: e["kany"] = kany
    faq.append(e)

# ------------------------------------------------------------------ KELIME-TEMELLI URETIM
for w in kelimeler:
    parts = hece_bol(w)
    nh = len(parts)
    nharf = len(w)
    ilk = tr_upper(w[0]); son = tr_upper(w[-1])
    ns, nz = n_sesli(w), n_sessiz(w)
    # 1) heceleme
    add(f"{w} hecele", f"**{w}** → {' - '.join(parts)} ({nh} hece) 😊", w=w, k=["hecele"])
    # 2) hece sayisi — yalnizca gercek sayim sorusunda tetiklensin (kac hece / heceli / hece sayisi)
    add(f"{w} kaç hecelidir?", f"**{w}** kelimesi **{nh}** hecelidir: {'-'.join(parts)} 😊", w=w, kany=["kaç hece", "heceli", "hecesi", "hece sayı"])
    # 3) harf sayisi — yalnizca gercek sayim sorusunda tetiklensin (kac harf / harfli / harf sayisi)
    add(f"{w} kaç harflidir?", f"**{w}** kelimesinde **{nharf}** harf vardır. 😊", w=w, kany=["kaç harf", "harfli", "harf sayı"])
    # 4) ilk harf — "ilk harf" ifadesi gecmeli
    add(f"{w} kelimesinin ilk harfi nedir?",
        f"**{w}** kelimesinin ilk harfi **{ilk}** harfidir. 😊", w=w, k=["ilk harf"])
    # 5) son harf — "son harf" ifadesi gecmeli
    add(f"{w} kelimesinin son harfi nedir?",
        f"**{w}** kelimesinin son harfi **{son}** harfidir. 😊", w=w, k=["son harf"])

# ------------------------------------------------------------------ IMLA CIFTLERI (dogru: yanlis)
IMLA = {
    "herkes": "herkez", "her şey": "herşey", "yalnız": "yanlız", "yanlış": "yalnış",
    "şu an": "şuan", "bir şey": "birşey", "hiçbir": "hiç bir", "birkaç": "bir kaç",
    "çünkü": "çünki", "her zaman": "herzaman", "her gün": "hergün", "sağ ol": "sağol",
    "hoş geldin": "hoşgeldin", "hoşça kal": "hoşçakal", "hafta sonu": "haftasonu",
    "hastane": "hastahane", "dakika": "dakka", "program": "proğram", "burada": "burda",
    "domates": "tomates", "maydanoz": "maydonoz", "meyve": "meyva", "çikolata": "çukulata",
    "bisküvi": "büsküvi", "gazete": "gaste", "fotoğraf": "fotograf", "film": "filim",
    "grup": "gurup", "seyahat": "seyehat", "kibrit": "kibirt", "yoğurt": "yourt",
    "inşallah": "inşaallah", "kestane": "kestene", "eczane": "ezcane",
    "ambulans": "ambülans", "şoför": "şöför", "direksiyon": "direksyon",
    "makine": "makina", "tıraş": "traş", "sürpriz": "süpriz",
}
INTENT = ["yaz", "doğru", "nasıl", "ayrı", "bitişik", "hangi", "yanlış", "imla"]
for dogru, yanlis in IMLA.items():
    a = f"Doğrusu **{dogru}**. ✍️ (\"{yanlis}\" yanlıştır.)"
    # dogru form: yalnizca yazim niyeti varsa cevapla (gunluk kullanimda tetiklenmesin)
    add(f"{dogru} nasıl yazılır?", a, w=dogru, kany=INTENT)
    # yanlis yazim her gectiginde duzelt
    add(f"{yanlis} mı {dogru} mu?", a, w=yanlis)

# ------------------------------------------------------------------ DE/DA, KI, MI KURALLARI
add("de da nasıl yazılır?",
    "Bağlaç olan **de/da** ayrı yazılır: \"Ali **de** geldi.\" Hâl eki olan -de/-da bitişik: \"okul**da**\". 😊",
    w="de", kany=["yaz", "ayrı", "bitişik", "nasıl", "kural"])
add("ki bağlacı nasıl yazılır?",
    "Bağlaç olan **ki** ayrı yazılır: \"Duydum **ki** gelmişsin.\" 😊",
    w="ki", kany=["yaz", "ayrı", "nasıl", "bağlaç"])
add("mi soru eki nasıl yazılır?",
    "Soru eki **mı/mi/mu/mü** her zaman ayrı yazılır: \"Geldin **mi**?\" 😊",
    w="mi", kany=["yaz", "ayrı", "soru", "ek"])

# ------------------------------------------------------------------ KURAL / TANIM / NOKTALAMA / BUYUK HARF
KURALLAR = [
    ("sesli harfler nelerdir",
     "Sesli (ünlü) harfler: a, e, ı, i, o, ö, u, ü. Toplam **8** tane! 😊",
     None, ["sesli"], None),
    ("sessiz harfler nelerdir",
     "Sessiz (ünsüz) harfler: b, c, ç, d, f, g, ğ, h, j, k, l, m, n, p, r, s, ş, t, v, y, z. Toplam **21** tane! 😊",
     None, ["sessiz"], None),
    ("alfabede kaç harf var",
     "Türk alfabesinde **29** harf vardır: **8** sesli, **21** sessiz. 😊",
     None, ["alfabe"], None),
    ("alfabe sırası nedir",
     "Türk alfabesi: a b c ç d e f g ğ h ı i j k l m n o ö p r s ş t u ü v y z. 😊",
     None, ["alfabe", "sıra"], None),
    ("ğ harfi ile kelime başlar mı",
     "Hayır, Türkçede hiçbir kelime **ğ** harfiyle **başlamaz**. 😊",
     "ğ", None, ["başla"]),
    ("nokta nereye konur",
     "**Nokta (.)** cümlenin sonuna konur. Örnek: Bugün hava çok güzel. 😊",
     None, ["nokta"], None),
    ("virgül nereye konur",
     "**Virgül (,)** sıralanan kelimeleri ayırır. Örnek: Elma, armut ve muz aldım. 😊",
     None, ["virgül"], None),
    ("soru işareti nereye konur",
     "**Soru işareti (?)** soru cümlesinin sonuna konur. Örnek: Adın ne? 😊",
     None, ["soru işaret"], None),
    ("ünlem işareti ne zaman konur",
     "**Ünlem (!)** sevinç, heyecan veya seslenme bildirir. Örnek: Yaşasın! 😊",
     None, ["ünlem"], None),
    ("iki nokta ne zaman konur",
     "**İki nokta (:)** bir açıklama veya örnek sıralanacağında konur. Örnek: Şunları aldım: kalem, defter. 😊",
     None, ["iki nokta"], None),
    ("kesme işareti ne zaman konur",
     "**Kesme işareti (')** özel isimlere gelen ekleri ayırır. Örnek: Ankara'da, Ali'nin. 😊",
     None, ["kesme"], None),
    ("büyük harf ne zaman kullanılır",
     "Büyük harf iki yerde: 1) **Cümle başında** (Ali okula gitti.) 2) **Özel isimlerde** (Ali, İzmir, Türkiye). 👍",
     None, ["büyük harf"], None),
    ("büyük ve küçük harf nedir",
     "**Büyük harfler**: A, B, C, Ç… **Küçük harfler**: a, b, c, ç… Cümle **büyük** harfle başlar, özel isimler büyük yazılır (Ali, Ankara). Kelimenin geri kalanı küçük harfle yazılır. 😊",
     None, ["harf"], ["büyük küçük", "küçük büyük", "büyük ve küçük", "küçük ve büyük", "büyük harf", "küçük harf"]),
    ("gün ve ay adları büyük harfle mi yazılır",
     "Cümle içinde gün ve ay adları **küçük** harfle başlar: \"pazartesi\", \"ocak\". Ama belirli bir tarihle birlikte büyük yazılır: \"29 Mayıs\". 😊",
     None, ["gün", "ay"], None),
    ("özel isim nedir",
     "Özel isim, tek bir varlığa verilen addır: kişi (Ali), şehir (Bursa), ülke (Türkiye), hayvan adı (Tekir). Büyük harfle başlar. 😊",
     None, ["özel isim"], None),
    ("kelime nedir",
     "**Kelime (sözcük)**, anlamı olan ses ya da harf topluluğudur. Örnek: ev, okul, kalem. 😊",
     None, ["kelime nedir"], None),
    ("cümle nedir",
     "**Cümle**, bir duyguyu ya da düşünceyi tam anlatan kelimeler dizisidir. Büyük harfle başlar, noktalama ile biter. 😊",
     None, ["cümle nedir"], None),
    ("hece nedir",
     "**Hece**, ağzımızdan bir defada çıkan ses öbeğidir. Her hecede bir sesli harf vardır. Örnek: e-vi-miz. 😊",
     None, ["hece nedir"], None),
    ("hece nasıl bölünür",
     "Her hecede bir sesli vardır. İki sesli arasındaki tek sessiz sonraki heceye gider (a-ra-ba); iki sessiz yan yana bölünür (el-ma). 😊",
     None, ["hece"], ["böl", "ayır", "kural", "nasıl"]),
    ("noktalama işaretleri nelerdir",
     "Başlıca noktalama: nokta (.), virgül (,), soru işareti (?), ünlem (!), iki nokta (:), kesme ('). 😊",
     None, ["noktalama"], None),
    ("nasıl daha iyi okurum",
     "Her gün biraz oku, kelimeleri hecelemeden bütün gör, noktada kısa dur. Acele etme, anlayarak oku. 📖😊",
     None, ["oku"], ["nasıl", "daha iyi", "hızlı"]),
]
for q, a, w, k, kany in KURALLAR:
    add(q, a, w=w, k=k, kany=kany)

# ------------------------------------------------------------------ TEKILLESTIR + YAZ
uniq, qseen = [], set()
for e in faq:
    key = e["q"].lower()
    if key not in qseen:
        qseen.add(key); uniq.append(e)

js = "// OTOMATIK URETILDI — gen_faq.py. Elle duzenleme yerine betigi calistir.\n"
js += "// Soru bankasi: hazir, TDK-dogru cevaplar. Once buna bakilir; yoksa Gemini'ye sorulur.\n"
js += f"// Toplam kayit: {len(uniq)}\n"
js += "window.OW_FAQ = [\n"
for e in uniq:
    js += json.dumps(e, ensure_ascii=False) + ",\n"
js += "];\n"

with open("faq.js", "w", encoding="utf-8") as f:
    f.write(js)

print(f"faq.js olusturuldu. Toplam kayit: {len(uniq)}")
print(f"  - Kelime sayisi: {len(kelimeler)}")
print(f"  - Imla cifti: {len(IMLA)}")
