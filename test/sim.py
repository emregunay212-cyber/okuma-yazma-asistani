# -*- coding: utf-8 -*-
"""
sim.py — okuma-yazma-asistani.html'deki GUNCEL deterministik katmanin + konu-disi
kapisinin BIREBIR Python portu (localAnswer, onTopic, faqLookup, heceBol).
Kod surumune sadik kalmak icin HTML degisirse buradaki port da guncellenmeli.
"""
import re, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

V_SET = set("aeıioöuüAEIİOÖUÜ")
SESLI = list("aeıioöuü")
SESSIZ = list("bcçdfgğhjklmnprsştvyz")  # 21

def trLower(s):
    s = (s or "")
    s = (s.replace("İ", "i").replace("I", "ı").replace("Ş", "ş").replace("Ğ", "ğ")
           .replace("Ü", "ü").replace("Ö", "ö").replace("Ç", "ç"))
    return s.lower()

def trUpper(ch):
    return "İ" if ch == "i" else ("I" if ch == "ı" else ch.upper())

def fold(s):
    return (s.replace("ç", "c").replace("ğ", "g").replace("ı", "i")
             .replace("ö", "o").replace("ş", "s").replace("ü", "u"))

def heceBol(w):
    w = (w or "").strip()
    vi = [i for i, ch in enumerate(w) if ch in V_SET]
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

# ---- FAQ bankasi ----
def load_faq():
    with open(os.path.join(ROOT, "faq.js"), encoding="utf-8") as f:
        txt = f.read()
    arr = txt[txt.index("["):txt.rindex("]") + 1]
    arr = re.sub(r",\s*\]", "]", arr)
    return json.loads(arr)

OW_FAQ = load_faq()
_FFAQ = []
for e in OW_FAQ:
    w = e.get("w") or None  # GUNCEL: w foldLANMAZ (Turkce tam eslesir)
    k = [fold(x) for x in e["k"]] if e.get("k") else None
    kany = [fold(x) for x in e["kany"]] if e.get("kany") else None
    sc = (len(e["w"]) if e.get("w") else 0) + \
         (len("".join(fold(x) for x in e["k"])) if e.get("k") else 0)
    _FFAQ.append({"a": e["a"], "w": w, "k": k, "kany": kany, "sc": sc})

def faqLookup(t):
    normT = " " + re.sub(r"[^a-zçğıiöşü]+", " ", t).strip() + " "   # Turkce korunur (w icin)
    normF = " " + re.sub(r"[^a-z]+", " ", fold(t)).strip() + " "    # foldlu (k/kany icin)
    best, score = None, -1
    for e in _FFAQ:
        if e["w"] and (" " + e["w"] + " ") not in normT:
            continue
        if e["k"] and not all(kw in normF for kw in e["k"]):
            continue
        if e["kany"] and not any(kw in normF for kw in e["kany"]):
            continue
        if not e["w"] and not e["k"] and not e["kany"]:
            continue
        if e["sc"] > score:
            best, score = e, e["sc"]
    return best["a"] if best else None

WSTOP = set(["kaç", "hece", "kelime", "kelimede", "kelimesinde", "kelimesinin",
             "kelimenin", "bu", "bir", "ilk", "son", "sesli", "sessiz", "harf",
             "harfi", "var", "kaçtane", "alfabe", "alfabede", "alfabenin",
             "türkçe", "türkçede", "türkçenin", "cümle", "cümlede", "sözcük",
             "mı", "mi", "mu", "mü", "nin", "nın", "nun", "nün"])
WSTOPf = set(fold(x) for x in WSTOP)

TOPIC_WORDS = ["harf", "ses", "ünlü", "ünsüz", "alfabe", "hece", "kelime",
               "sözcük", "cümle", "imla", "yazım", "yaz", "oku", "dikte",
               "nokta", "virgül", "noktalama", "ünlem", "vurgu", "satır",
               "şiir", "tekerleme", "metin", "paragraf", "türkçe"]

def onTopic(text):
    t = fold(trLower(text or ""))
    return any(fold(w) in t for w in TOPIC_WORDS)

def localAnswer(text):
    t = re.sub(r"['’ʼ]", "", trLower(text))
    tf = fold(t)

    # Karşılaştırma sorusu mu? -> tek kelimeye deterministik cevap verme (yanlış-kelime yakalamayı önler)
    # "hangi"/iki soru eki yalnızca sayım-uzunluk bağlamıyla karşılaştırma sayılır (imla düzeltmelerini korur)
    cnt = bool(re.search(r"(kac|harf|hece|uzun|kisa|fazla|buyuk|kucuk)", tf))
    cmp = (bool(re.search(r"\bhangi", tf)) and cnt) \
        or (len(re.findall(r"\bm[iu]\b", tf)) >= 2 and cnt) \
        or bool(re.search(r"\bdaha\s+(cok|fazla|az|uzun|kisa|buyuk|kucuk)", tf)) \
        or bool(re.search(r"kac\s*(harf|hece)\s*(fazla|uzun|kisa|az|cok)", tf))

    # Tek harf: "X (harfi) sesli/sessiz mi" / "X harfi nedir"
    lm = re.search(r"(?:^|[\s\"'(])([a-z])\s*(?:harfi?\s*)?(?:sesli|unlu|sessiz|unsuz)\s*m[iu]", tf) \
        or re.search(r"(?:^|[\s\"'(])([a-z])\s*harfi?\s*(?:ne|nedir)", tf)
    if lm:
        s, e = lm.span(1); h = t[s:e]
        if h in SESLI:
            return f"**{trUpper(h)}** harfi **sesli (ünlü)** harftir. 😊"
        if h in SESSIZ:
            return f"**{trUpper(h)}** harfi **sessiz (ünsüz)** harftir. 😊"

    def wq(pat):
        if cmp:
            return None
        m = re.search(pat, tf)
        if not m:
            return None
        s, e = m.span(1); w = t[s:e]; fw = fold(w)
        if fw in WSTOPf or re.match(r"^(alfabe|turkce|kelime|sozcuk|cumle)", fw):
            return None
        return w

    w = wq(r"([a-z]{2,})\s+(?:kelimesin(?:in|de)\s+)?ilk harf")
    if w:
        return f"**{w}** kelimesinin ilk harfi **{trUpper(w[0])}** harfidir. 😊"
    w = wq(r"([a-z]{2,})\s+(?:kelimesin(?:in|de)\s+)?son harf")
    if w:
        return f"**{w}** kelimesinin son harfi **{trUpper(w[-1])}** harfidir. 😊"
    w = wq(r"([a-z]{2,})\s+(?:kelimesinde\s+)?kac\s*(?:sessiz|unsuz)")
    if w:
        n = sum(1 for c in w if c in SESSIZ)
        return f"**{w}** kelimesinde **{n}** sessiz harf vardır. 😊"
    w = wq(r"([a-z]{2,})\s+(?:kelimesinde\s+)?kac\s*(?:sesli|unlu)")
    if w:
        n = sum(1 for c in w if c in SESLI)
        return f"**{w}** kelimesinde **{n}** sesli harf vardır. 😊"
    w = wq(r"([a-z]{1,})\s+(?:kelimesinde\s+)?kac\s*harf")
    if w:
        return f"**{w}** kelimesinde **{len(w)}** harf vardır. 😊"

    wantsSesli = bool(re.search(r"(sesli|unlu)", tf)) and bool(re.search(r"harf", tf))
    wantsSessiz = bool(re.search(r"(sessiz|unsuz)", tf)) and bool(re.search(r"harf", tf))
    if wantsSesli and wantsSessiz:
        return "Sesli (ünlü) harfler: " + ", ".join(SESLI) + " → **8** tane.\nSessiz (ünsüz) harfler: " + ", ".join(SESSIZ) + " → **21** tane. 😊"
    if wantsSesli:
        return "Sesli (ünlü) harfler: " + ", ".join(SESLI) + ". Toplam **8** tane! 😊"
    if wantsSessiz:
        return "Sessiz (ünsüz) harfler: " + ", ".join(SESSIZ) + ". Toplam **21** tane! 😊"

    fq = None if cmp else faqLookup(t)
    if fq is not None:
        return fq

    if re.search(r"hece", tf) and not cmp:
        m = (re.search(r"([a-z]{2,})\s+(?:kelimesini\s+|kelimesi\s+)?hecele", tf)
             or re.search(r"hecele\s+(?:bana\s+|su\s+)?([a-z]{2,})", tf)
             or re.search(r"([a-z]{2,})\s+(?:kelimesi\s+)?kac\s*hece", tf))
        skip = set(["kelime", "kelimesini", "kelimesi", "bana", "su", "bir", "lutfen"])
        if m:
            s, e = m.span(1); word = t[s:e]; fw = fold(word)
            if fw not in skip and not re.match(r"^(hece|bol|ayir)", fw):
                parts = heceBol(word)
                if re.search(r"kac\s*hece", tf):
                    return f"**{word}** kelimesinde **{len(parts)}** hece var: {'-'.join(parts)} 😊"
                return f"**{word}** → {' - '.join(parts)} ({len(parts)} hece) 😊"
        return "Hece bölme kuralı: Her hecede **bir sesli harf** vardır. İki sesli arasındaki tek sessiz sonraki heceye gider (a-ra-ba); iki sessiz yan yana ise bölünür (el-ma, kar-tal). Örnek: top (1), el-ma (2), ke-le-bek (3). 😊"

    if re.search(r"alfabe", tf) and re.search(r"kac harf|kac tane|harf say", tf):
        return "Türk alfabesinde **29** harf vardır: **8** sesli (" + ", ".join(SESLI) + ") ve **21** sessiz harf. 😊"

    if re.search(r"buyuk harf", tf):
        return "Büyük harf iki yerde kullanılır:\n1) **Cümle başında**: Ali okula gitti.\n2) **Özel isimlerde**: Ali, Ayşe, İzmir, Türkiye. 👍"

    pi = bool(re.search(r"(nereye|ne zaman|nasil|nedir|ne demek|konur|koy|kullanil|ne ise|sonun|isaret|biter)", tf))
    if re.search(r"nokta", tf) and not re.search(r"noktalama", tf) and pi:
        return "**Nokta (.)** cümlenin sonuna konur. Örnek: Bugün hava çok güzel. 😊"
    if re.search(r"virgul", tf) and pi:
        return "**Virgül (,)** sıralanan kelimeleri birbirinden ayırır. Örnek: Elma, armut ve muz aldım. 😊"
    if re.search(r"soru isaret", tf) and pi:
        return "**Soru işareti (?)** soru cümlesinin sonuna konur. Örnek: Adın ne? 😊"
    if re.search(r"unlem", tf) and pi:
        return "**Ünlem işareti (!)** sevinç, heyecan veya seslenme bildirir. Örnek: Yaşasın! 😊"
    if re.search(r"noktalama", tf):
        return "Noktalama işaretleri:\n• **Nokta (.)** → cümle sonu\n• **Virgül (,)** → sıralama\n• **Soru işareti (?)** → soru sonu\n• **Ünlem (!)** → heyecan/seslenme 😊"

    if re.search(r"imla|yazim kural", tf):
        return "Önemli imla kuralları:\n• Cümle **büyük harfle** başlar, **nokta** ile biter.\n• Özel isimler büyük harfle yazılır: Ali, Ankara.\n• \"de/da\" bağlacı ayrı yazılır: \"Ali de geldi.\" 😊"

    if re.search(r"dikte", tf):
        return "[DİKTE: rastgele 10 kelime listesi]"

    return None

def classify(text):
    a = localAnswer(text)
    if a is not None:
        return ("deterministik", a)
    if not onTopic(text):
        return ("konu-dışı yönlendirme",
                "Ben okuma-yazma asistanıyım 😊 Sana harfler, heceler, kelimeler, cümleler ve yazım konularında yardımcı olabilirim. Bunlardan birini sormak ister misin?")
    return ("model", "[MODEL: Gemini 2.5 Flash Lite — sistem promptuna göre yanıt]")


if __name__ == "__main__":
    tests = [
        ("araba kaç hece", "deterministik", "3"),
        ("elma hecele", "deterministik", "el - ma"),
        ("b harfi sesli mi", "deterministik", "sessiz"),
        ("b ünsüz mü", "deterministik", "sessiz"),          # GUNCEL: m[iu] -> calismali
        ("a sesli mi", "deterministik", "sesli"),
        ("sesli harfler neler", "deterministik", "8"),
        ("alfabede kaç harf var", "deterministik", "29"),
        ("kalem kaç sesli", "deterministik", "2"),
        ("ışık kaç harf", "deterministik", "4"),
        ("isik kac harf", "deterministik", "4"),            # GUNCEL: foldlu tf -> calismali
        ("kalem kelimesinin ilk harfi nedir", "deterministik", "K"),
        ("g ile baslayan kelime olur mu", None, None),      # GUNCEL: 'g' != 'ğ' (normT Turkce)
        ("şu cümlede kaç harf var: Ali okula gitti", None, None),  # alfabe yok -> 29 OLMAMALI
        ("12345 kaç harf", None, None),
        ("Ali de geldi", "konu-dışı yönlendirme", None),
        ("futbol maçı kaçta", "konu-dışı yönlendirme", None),
    ]
    ok = 0
    for q, exp_layer, exp_sub in tests:
        layer, ans = classify(q)
        layer_ok = (exp_layer is None) or (layer == exp_layer)
        sub_ok = (exp_sub is None) or (exp_sub in (ans or ""))
        # ozel: "29 OLMAMALI" kontrolu
        extra_ok = True
        if q in ("şu cümlede kaç harf var: Ali okula gitti", "12345 kaç harf"):
            extra_ok = ("29" not in (ans or "")) or layer != "deterministik"
        if q == "g ile baslayan kelime olur mu":
            extra_ok = "başlamaz" not in (ans or "")
        good = layer_ok and sub_ok and extra_ok
        if good: ok += 1
        print(f"[{'OK ' if good else 'FAIL'}] {q!r}\n        -> ({layer}) {(ans or '')[:62].strip()!r}")
    print(f"\n{ok}/{len(tests)} gecti.")
