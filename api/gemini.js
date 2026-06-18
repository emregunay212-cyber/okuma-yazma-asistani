// Vercel Serverless Function — Gemini proxy.
// API anahtarı sunucuda (process.env.GEMINI_API_KEY) kalır, tarayıcıya gitmez.
// İstemci, Gemini'ye göndereceği gövdenin AYNISINI buraya POST eder.
module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.status(405).json({ error: { message: 'Yalnızca POST destekleniyor.' } });
    return;
  }
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    res.status(500).json({ error: { message: 'Sunucuda GEMINI_API_KEY tanımlı değil. Vercel ortam değişkenini ekleyin.' } });
    return;
  }
  try {
    const body = typeof req.body === 'string' ? req.body : JSON.stringify(req.body || {});
    const r = await fetch(
      'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key=' + key,
      { method: 'POST', headers: { 'Content-Type': 'application/json' }, body }
    );
    const data = await r.json();
    res.status(r.status).json(data);
  } catch (e) {
    res.status(500).json({ error: { message: String((e && e.message) || e) } });
  }
};
