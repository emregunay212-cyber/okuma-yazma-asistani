# -*- coding: utf-8 -*-
"""
build.py — test setini olusturur:
  1) Deterministik kategoriler icin PROGRAMATIK soru uretimi (cevaplar heceBol/sayim ile
     KESIN dogru hesaplanir; grade 1-2 kapsamindaki kelimelerde heceBol == TDK).
  2) Workflow'un urettigi YARATICI/TUZAK sorulari (test/questions_creative.json) eklenir.
  3) HER soru gercek mantiktan (sim.classify) gecirilir -> gercek_katman, gercek_cevap.
  4) beklenen vs gercek karsilastirilir -> durum (OK / BULGU).
  5) Cikti: test/test-sorulari.md + test/test-sorulari.json + ozet.
"""
import sys, os, json, re, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim import classify, heceBol, SESLI, SESSIZ, trUpper

HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(20260618)

# ---- kapsam-ici (grade 1-2), heceBol == TDK dogrulanmis kelimeler ----
CORE = ["elma", "kitap", "kalem", "okul", "masa", "kapı", "arı", "çiçek", "bulut",
        "tavuk", "kelebek", "karpuz", "limon", "balık", "kedi", "köpek", "aslan",
        "deniz", "güneş", "araba", "anne", "top", "defter", "silgi", "pencere"]
TRICKY = ["yağmur", "ışık", "iğne", "kitapçı", "gökyüzü", "ağaç", "şemsiye", "uçak",
          "oyuncak", "sınıf", "ağustos", "kütüphane", "bilgisayar", "televizyon",
          "öğretmen", "yoğurt"]
SINGLE = ["a", "e", "b", "ğ", "ı", "i", "v", "z", "m", "o", "ü", "ş", "r", "j"]

def strip_md(s):
    return s.replace("*", "")

def n_sesli(w):  return sum(1 for c in w if c in SESLI)
def n_sessiz(w): return sum(1 for c in w if c in SESSIZ)

rows = []  # her oge: dict (soru, kategori, beklenen_katman, beklenen_cevap, zorluk, neden_tuzak, _kontrol, _kaynak)

def add(soru, kategori, beklenen_katman, beklenen_cevap, zorluk, neden_tuzak="",
        kontrol=None, kaynak="programatik"):
    rows.append({
        "soru": soru, "kategori": kategori, "beklenen_katman": beklenen_katman,
        "beklenen_cevap": beklenen_cevap, "zorluk": zorluk, "neden_tuzak": neden_tuzak,
        "_kontrol": kontrol or [], "_kaynak": kaynak,
    })

# ============================================================ PROGRAMATIK DETERMINISTIK
# heceleme
hece_words = CORE[:14] + TRICKY
for i, w in enumerate(hece_words):
    parts = heceBol(w); nh = len(parts); hb = "-".join(parts)
    zor = "orta" if w in TRICKY else "kolay"
    if i % 3 == 0:
        add(f"{w} hecele", "heceleme", "deterministik",
            f"{w} → {hb} ({nh} hece)", zor, "", [w, f"{nh} hece"])
    elif i % 3 == 1:
        add(f"{w} kelimesini hecele", "heceleme", "deterministik",
            f"{w} → {hb} ({nh} hece)", zor, "", [w, f"{nh} hece"])
    else:
        add(f"{w} kaç hecelidir?", "heceleme", "deterministik",
            f"{nh} hece: {hb}", zor, "", [w, str(nh)])
# birkac "kaç hece" dolaysiz
for w in ["karpuz", "kütüphane", "şemsiye", "yağmur"]:
    parts = heceBol(w)
    add(f"{w} kaç hece", "heceleme", "deterministik",
        f"{len(parts)} hece: {'-'.join(parts)}", "orta", "", [w, str(len(parts))])

# harf sayımı (aksan-duyarsiz varyasyonlar dahil)
harf_words = CORE[:12] + TRICKY[:8]
for i, w in enumerate(harf_words):
    zor = "orta" if w in TRICKY else "kolay"
    if i % 2 == 0:
        add(f"{w} kaç harf", "harf sayımı", "deterministik",
            f"{len(w)} harf", zor, "", [w, f"{len(w)} harf"])
    else:
        add(f"{w} kaç harflidir?", "harf sayımı", "deterministik",
            f"{len(w)} harf", zor, "", [w, f"{len(w)} harf"])
# aksan-duyarsiz (Turkce karaktersiz yazim) — sistem yine de yakalamali
for w in ["balık", "ışık", "çiçek", "öğretmen"]:
    fold_q = w.replace("ç", "c").replace("ğ", "g").replace("ı", "i").replace("ö", "o").replace("ş", "s").replace("ü", "u")
    add(f"{fold_q} kac harf", "harf sayımı", "deterministik",
        f"{len(w)} harf ({w})", "tuzak",
        "Aksan-duyarsiz eslesme: Turkce karaktersiz yazim dogru yakalanmali", [f"{len(w)} harf"])

# sesli-sessiz
ss_words = CORE[:10] + TRICKY[:6]
for i, w in enumerate(ss_words):
    zor = "orta" if w in TRICKY else "kolay"
    if i % 2 == 0:
        add(f"{w} kaç sesli", "sesli-sessiz", "deterministik",
            f"{n_sesli(w)} sesli harf", zor, "", [w, f"{n_sesli(w)} sesli"])
    else:
        add(f"{w} kaç sessiz", "sesli-sessiz", "deterministik",
            f"{n_sessiz(w)} sessiz harf", zor, "", [w, f"{n_sessiz(w)} sessiz"])
# "kaç sesli harf var" uzun ifade
for w in ["kelebek", "gökyüzü"]:
    add(f"{w} kelimesinde kaç sesli harf var", "sesli-sessiz", "deterministik",
        f"{n_sesli(w)} sesli harf", "orta", "", [w, f"{n_sesli(w)} sesli"])

# ilk-son harf
is_words = CORE[:10] + TRICKY[:5]
for i, w in enumerate(is_words):
    zor = "orta" if w in TRICKY else "kolay"
    if i % 2 == 0:
        add(f"{w} ilk harf", "ilk-son harf", "deterministik",
            f"İlk harf: {trUpper(w[0])}", zor, "", [w, trUpper(w[0])])
    else:
        add(f"{w} son harf", "ilk-son harf", "deterministik",
            f"Son harf: {trUpper(w[-1])}", zor, "", [w, trUpper(w[-1])])
for w in ["kalem", "deniz"]:
    add(f"{w} kelimesinin ilk harfi nedir?", "ilk-son harf", "deterministik",
        f"İlk harf: {trUpper(w[0])}", "kolay", "", [w, trUpper(w[0])])

# tek harf turu
for i, L in enumerate(SINGLE):
    tip = "sesli (ünlü)" if L in SESLI else "sessiz (ünsüz)"
    if i % 3 == 0:
        add(f"{L} harfi sesli mi", "sesli-sessiz", "deterministik",
            f"{trUpper(L)} → {tip}", "kolay", "", [trUpper(L), "sesli" if L in SESLI else "sessiz"])
    elif i % 3 == 1:
        add(f"{L} sesli mi sessiz mi", "sesli-sessiz", "deterministik",
            f"{trUpper(L)} → {tip}", "kolay", "", [trUpper(L)])
    else:
        add(f"{L} ünsüz mü", "sesli-sessiz", "deterministik",
            f"{trUpper(L)} → {tip}", "kolay", "", [trUpper(L)])

# ============================================================ YARATICI/TUZAK (workflow)
creative_path = os.path.join(HERE, "questions_creative.json")
n_creative = 0
if os.path.exists(creative_path):
    with open(creative_path, encoding="utf-8") as f:
        data = json.load(f)
    for q in data.get("sorular", []):
        rows.append({
            "soru": q["soru"], "kategori": q.get("kategori", "?"),
            "beklenen_katman": q["beklenen_katman"], "beklenen_cevap": q.get("beklenen_cevap", ""),
            "zorluk": q.get("zorluk", "orta"), "neden_tuzak": q.get("neden_tuzak", ""),
            "_kontrol": [], "_kaynak": "workflow:" + q.get("_ajan", "?"),
        })
        n_creative += 1

# ============================================================ KATEGORI NORMALIZE
def norm_kat(k):
    kl = k.lower()
    if kl.startswith("sınır") or kl.startswith("sinir") or "aykırı" in kl:
        return "sınır/aykırı girdiler"
    if k == "heceleme/harf-sayımı":
        return "yanlış-kelime yakalama"
    return k
for r in rows:
    r["kategori"] = norm_kat(r["kategori"])

# ============================================================ DEDUPE
seen = set(); uniq = []
for r in rows:
    key = re.sub(r"\s+", " ", r["soru"].strip().lower())
    if key and key not in seen:
        seen.add(key); uniq.append(r)
rows = uniq

# ============================================================ GERCEK MANTIKTAN GECIR
# durum tipleri:
#   OK            -> beklenen == gercek (ve programatik degerler dogru)
#   YANLIŞ-DEĞER  -> dogru katman ama beklenen sayi/harf cevapta yok (yanlis kelime/sayim) [YUKSEK GUVEN BUG]
#   YANLIŞ-RED    -> gecerli soru haksizca konu-disi'na yonlendirildi                       [CIDDI]
#   SIZINTI       -> konu-disi olmasi gereken soru cevaplandi/modele gitti                  [CIDDI]
#   DET-KAÇIŞ     -> deterministik beklenirken modele dustu (model yine de cevaplar)        [HAFIF/kapsam]
#   DET-FAZLA     -> model beklenirken deterministik tetiklendi (yanlis-kelime riski)       [INCELE]
KONU = "konu-dışı yönlendirme"
for r in rows:
    layer, ans = classify(r["soru"])
    r["gercek_katman"] = layer
    r["gercek_cevap"] = ans
    bk = r["beklenen_katman"]
    if bk == layer:
        ok = True; missing = []
        stripped = strip_md(ans).lower()
        for kc in r["_kontrol"]:
            if kc.lower() not in stripped:
                ok = False; missing.append(kc)
        if ok:
            r["durum"] = "OK"; r["bulgu_not"] = ""
        else:
            r["durum"] = "YANLIŞ-DEĞER"
            r["bulgu_not"] = "Beklenen değer cevapta yok (yanlış kelime/sayım): eksik=" + ", ".join(missing)
    elif layer == KONU and bk != KONU:
        r["durum"] = "YANLIŞ-RED"
        r["bulgu_not"] = f"Geçerli soru konu-dışına yönlendirildi (beklenen {bk})"
    elif bk == KONU and layer != KONU:
        r["durum"] = "SIZINTI"
        r["bulgu_not"] = f"Konu-dışı olması gereken soru '{layer}' katmanına gitti"
    elif bk == "deterministik" and layer == "model":
        r["durum"] = "DET-KAÇIŞ"
        r["bulgu_not"] = "Deterministik beklenirken modele düştü (model yanıtlayabilir)"
    elif bk == "model" and layer == "deterministik":
        r["durum"] = "DET-FAZLA"
        r["bulgu_not"] = "Model beklenirken deterministik tetiklendi (yanlış-kelime yakalama riski)"
    else:
        r["durum"] = "UYUŞMAZLIK"
        r["bulgu_not"] = f"beklenen={bk}, gerçek={layer}"

OK_SET = {"OK"}
CIDDI = {"YANLIŞ-DEĞER", "YANLIŞ-RED", "SIZINTI"}

# ============================================================ CIKTI: JSON
out_json = os.path.join(HERE, "test-sorulari.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump([{k: v for k, v in r.items() if k != "_kontrol"} for r in rows],
              f, ensure_ascii=False, indent=2)

# ============================================================ CIKTI: MARKDOWN
KAT_SIRA = ["heceleme", "harf sayımı", "sesli-sessiz", "ilk-son harf",
            "yanlış-kelime yakalama", "imla", "noktalama", "büyük harf", "alfabe",
            "FAQ-kural", "konu-dışı", "sınır/aykırı girdiler", "?"]
def kat_key(k):
    for i, x in enumerate(KAT_SIRA):
        if k.lower().startswith(x.lower()) or x.lower() in k.lower():
            return i
    return len(KAT_SIRA)

cats = {}
for r in rows:
    cats.setdefault(r["kategori"], []).append(r)

n_total = len(rows)
n_ok = sum(1 for r in rows if r["durum"] in OK_SET)
n_bulgu = n_total - n_ok
n_ciddi = sum(1 for r in rows if r["durum"] in CIDDI)
zor_say = {z: sum(1 for r in rows if r["zorluk"] == z) for z in ["kolay", "orta", "tuzak"]}
kat_say = {k: len(v) for k, v in cats.items()}
durum_say = {}
for r in rows:
    durum_say[r["durum"]] = durum_say.get(r["durum"], 0) + 1

md = []
DTAN = {
    "YANLIŞ-DEĞER": "Doğru katman ama yanlış kelime/sayım (yüksek güven bug)",
    "YANLIŞ-RED": "Geçerli soru haksızca konu-dışına yönlendirildi",
    "SIZINTI": "Konu-dışı olması gereken soru cevaplandı/modele gitti",
    "DET-KAÇIŞ": "Deterministik beklenirken modele düştü (kapsam açığı; model yine yanıtlar)",
    "DET-FAZLA": "Model beklenirken deterministik tetiklendi (yanlış-kelime yakalama riski — incele)",
    "UYUŞMAZLIK": "Diğer yönlendirme uyuşmazlığı",
}
md.append("# Okuma Yazma Asistanı — Test/QA Soru Seti\n")
md.append(f"> Toplam **{n_total}** soru. Her soru sistemin GERÇEK mantığından "
          f"(`test/sim.py` — `localAnswer`+`onTopic`+`faqLookup`'un birebir Python portu) "
          f"geçirilmiştir; `beklenen` (TDK-doğru/ideal davranış) ile `gerçek` "
          f"(sistemin fiilen yaptığı) karşılaştırılır.\n")
md.append(f"> **Geçen (OK): {n_ok}/{n_total}** · **Uyuşmazlık: {n_bulgu}** "
          f"(bunların {n_ciddi} tanesi CİDDİ: yanlış değer / yanlış red / sızıntı).\n")
md.append("\n## Özet\n")
md.append("| Zorluk | Adet |")
md.append("|--------|------|")
for z in ["kolay", "orta", "tuzak"]:
    md.append(f"| {z} | {zor_say[z]} |")
md.append("\n| Durum | Adet | Anlamı |")
md.append("|-------|------|--------|")
md.append(f"| OK | {n_ok} | beklenen = gerçek |")
for d in ["YANLIŞ-DEĞER", "YANLIŞ-RED", "SIZINTI", "DET-FAZLA", "DET-KAÇIŞ", "UYUŞMAZLIK"]:
    if durum_say.get(d):
        md.append(f"| {d} | {durum_say[d]} | {DTAN[d]} |")
md.append("\n| Kategori | Adet | Uyuşmazlık |")
md.append("|----------|------|------------|")
for k in sorted(cats, key=kat_key):
    b = sum(1 for r in cats[k] if r["durum"] not in OK_SET)
    md.append(f"| {k} | {len(cats[k])} | {b} |")

# Bulgular — tipe gore grupla
bulgular = [r for r in rows if r["durum"] not in OK_SET]
if bulgular:
    md.append("\n## ⚠️ Bulgular (sistem ideal davranıştan sapıyor)\n")
    md.append("Önem sırasına göre gruplanmıştır. CİDDİ olanlar gerçek bug adayıdır; "
              "DET-KAÇIŞ/DET-FAZLA çoğu zaman tartışmalıdır (model yine doğru yanıtlayabilir).\n")
    for d in ["YANLIŞ-DEĞER", "YANLIŞ-RED", "SIZINTI", "DET-FAZLA", "DET-KAÇIŞ", "UYUŞMAZLIK"]:
        grp = [r for r in bulgular if r["durum"] == d]
        if not grp:
            continue
        md.append(f"\n### {d} — {DTAN[d]} ({len(grp)})\n")
        md.append("| # | Soru | Beklenen | Gerçek | Gerçek cevap (kısalt.) |")
        md.append("|---|------|----------|--------|------------------------|")
        for i, r in enumerate(grp, 1):
            gc = strip_md(r["gercek_cevap"]).replace("\n", " ").replace("|", "\\|")[:55]
            soru = r["soru"].replace("|", "\\|")
            md.append(f"| {i} | `{soru}` | {r['beklenen_katman']} | {r['gercek_katman']} | {gc} |")

# Tam liste — kategori bazli
md.append("\n## Tam Soru Listesi\n")
for k in sorted(cats, key=kat_key):
    md.append(f"\n### {k} ({len(cats[k])})\n")
    md.append("| Soru | Beklenen katman | Beklenen cevap | Zorluk | Gerçek katman | Durum | Tuzak nedeni |")
    md.append("|------|-----------------|----------------|--------|---------------|-------|--------------|")
    for r in cats[k]:
        gc = strip_md(r["gercek_cevap"]).replace("\n", " ")[:60]
        soru = r["soru"].replace("|", "\\|")
        bc = r["beklenen_cevap"].replace("|", "\\|").replace("\n", " ")[:50]
        nt = r["neden_tuzak"].replace("|", "\\|").replace("\n", " ")[:70]
        dd = "✅" if r["durum"] in OK_SET else "⚠️ " + r["durum"]
        md.append(f"| {soru} | {r['beklenen_katman']} | {bc} | {r['zorluk']} | {r['gercek_katman']} | {dd} | {nt} |")

out_md = os.path.join(HERE, "test-sorulari.md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")

# ============================================================ OZET (stdout)
print(f"Toplam soru: {n_total}  (OK={n_ok}, uyusmazlik={n_bulgu}, ciddi={n_ciddi})")
print(f"  Zorluk: " + ", ".join(f"{z}={zor_say[z]}" for z in zor_say))
print(f"  Programatik: {sum(1 for r in rows if r['_kaynak']=='programatik')}, "
      f"Workflow: {sum(1 for r in rows if r['_kaynak'].startswith('workflow'))}")
print(f"  Durum: " + ", ".join(f"{d}={durum_say[d]}" for d in sorted(durum_say)))
print(f"  Kategori: " + ", ".join(f"{k}={v}" for k, v in sorted(kat_say.items())))
print("\n--- CIDDI bulgular ---")
for r in rows:
    if r["durum"] in CIDDI:
        print(f"  [{r['durum']}] {r['soru']!r} -> ({r['gercek_katman']}) {strip_md(r['gercek_cevap'])[:45].strip()}")
print("\n--- DET-FAZLA (yanlis-kelime yakalama riski; incele) ---")
for r in rows:
    if r["durum"] == "DET-FAZLA":
        print(f"  {r['soru']!r} -> {strip_md(r['gercek_cevap'])[:45].strip()}")
print(f"\nYazildi: {out_md}")
print(f"Yazildi: {out_json}")
