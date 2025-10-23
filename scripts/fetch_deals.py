import os, json, feedparser, datetime

def now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"

def parse_feed(url):
    print(f"🔗 Leyendo feed: {url}")
    feed = feedparser.parse(url)
    items = []
    for e in feed.entries:
        items.append({
            "title": e.get("title", "Sin título"),
            "description": e.get("summary", ""),
            "url": e.get("link", ""),
            "published_at": e.get("published", now_iso()),
            "network": url.split("/")[2],
        })
    print(f"✅ {len(items)} ofertas capturadas de {url}")
    return items

def main():
    feeds_json = os.environ.get("FEED_URLS", "[]")
    feeds = json.loads(feeds_json)
    all_items = []

    if not feeds:
        print("⚠️ No hay feeds definidos en FEED_URLS.")
    else:
        for url in feeds:
            try:
                all_items.extend(parse_feed(url))
            except Exception as e:
                print(f"❌ Error en {url}: {e}")

    os.makedirs("site", exist_ok=True)
