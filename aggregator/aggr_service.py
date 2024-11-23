from aggregator import retrieve_feed
# from scraper import automate_links
# from article_extractor import filter_html
import json
import time

RSS_URL = [
    "https://rss.app/feeds/v1.1/wooXvaji9Y6z0rB1.json",  # Google
    "https://rss.app/feeds/v1.1/8LS0ifUfWFdE4zgj.json",  # BBC
    "https://rss.app/feeds/v1.1/jfGvnnaGk9xLumPS.json",  # insideevs
    "https://rss.app/feeds/v1.1/IRpIMtUGLmyhuGZv.json"
]

OUTPUT_PREFIX = "checkpoints/aggregate"

count = 1


def new_name() -> str:
    global count
    res = f"{OUTPUT_PREFIX}-{count}.json"
    count += 1
    return res


def prev_name() -> str:
    global count
    return f"{OUTPUT_PREFIX}-{count-1}.json"


def isDuplicate(articles, url):
    for article in articles:
        if article["url"] == url:
            return True
    return False


def merge_feeds(old, recent):
    """
    merge in place
    """
    for article in recent:
        if not isDuplicate(old, article["url"]):
            old = [article] + old

    return old


while True:
    articles_feed = []
    for feed in RSS_URL:
        articles_feed += retrieve_feed(feed)

    found_new = True

    if count > 0:
        with open(prev_name(), "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            old_len = len(data)
            articles_feed = merge_feeds(data, articles_feed)
            if not len(articles_feed) > old_len:
                print(
                    f"\tNo new articles found: {old_len} - {len(articles_feed)}")
                found_new = False

    if found_new:
        with open(new_name(), "w", encoding="utf-8") as json_file:
            json.dump(articles_feed, json_file, indent=4, ensure_ascii=False)

    print(
        f"FEED iteration {count}: total of {len(articles_feed)} unique articles")
    time.sleep(10*60)
