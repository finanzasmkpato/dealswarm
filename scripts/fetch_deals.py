import os, json, feedparser, datetime, traceback

def now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"

def parse_feed(url):
    print(f"🔗 Leyendo feed: {url}")
    feed = feedparser.parse(url)
    items = []
    for e in feed.entries:
        items.append({
            "title": e.get("title", "Sin título"),
            "description": e.get("summary", "") or e.get("description", ""),
            "url": e.get("link", ""),
            "published_at": e.get("published", now_iso()),
            "network": url.split("/")[2],
        })
    print(f"✅ {len(items)} ofertas capturadas de {url}")
    return items

def main():
    try:
        feeds_json = os.environ.get("FEED_URLS", "[]")
        feeds = json.loads(feeds_json)
    except Exception as e:
        print("⚠️ Error leyendo FEED_URLS:", e)
        feeds = []

    all_items = []

    if not feeds:
        print("⚠️ No hay feeds definidos en FEED_URLS. Se generará archivo vacío.")
    else:
        for url in feeds:
            try:
                all_items.extend(parse_feed(url))
            except Exception as e:
                print(f"❌ Error procesando {url}: {e}")
                traceback.print_exc()

    os.makedirs("site", exist_ok=True)
    output_path = "site/deals.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": now_iso(),
            "count": len(all_items),
            "items": all_items
        }, f, ensure_ascii=False, indent=2)

    print(f"💾 Archivo creado: {output_path} ({len(all_items)} ofertas)")

if __name__ == "__main__":
    main()
