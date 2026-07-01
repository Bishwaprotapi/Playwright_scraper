import feedparser
import requests
from scraper.config import RSS_FEEDS


def scrape_prothomalo():
    results = []

    for category, feed_url in RSS_FEEDS.items():
        print(f"Fetching RSS: {feed_url}")

        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            title = entry.get("title")
            link = entry.get("link")

            if not title or not link:
                continue

            # Try to extract image from RSS (media:content)
            image_url = None
            if "media_content" in entry:
                media = entry.media_content
                if isinstance(media, list) and len(media) > 0:
                    image_url = media[0].get("url")

            # Fallback: try og:image from article page
            if not image_url:
                try:
                    r = requests.get(link, timeout=10)
                    if r.ok:
                        text = r.text
                        if 'property="og:image"' in text:
                            image_url = text.split('property="og:image"')[1] \
                                .split('content="')[1] \
                                .split('"')[0]
                except Exception:
                    pass

            results.append({
                "title": title.strip(),
                "image_url": image_url,
                "article_link": link
            })

    # Remove duplicates
    unique = {}
    for item in results:
        unique[item["article_link"]] = item

    return list(unique.values())
