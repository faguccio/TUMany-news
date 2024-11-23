from aggregator import retrieve_feed
from scraper import automate_links
from article_extractor import filter_html
import json

RSS_URL = "https://rss.app/feeds/u6rcvfy6PTSf9vQ4.json"
LENGTH_CUTOUT = 10000

# Each article contain important metadata
# articles_feed = retrieve_feed(RSS_URL)

articles_feed = None

with open("aggregate.json", "r", encoding="utf-8") as json_file:
    articles_feed = json.load(json_file)

# Extract HTML from each article
articles_feed = automate_links(articles_feed)

result_feed = []
for article in articles_feed:
    article["html"] = filter_html(article["html"])
    if len(article["html"]) < LENGTH_CUTOUT:
        result_feed += [article]


with open("output.json", "w", encoding="utf-8") as json_file:
    json.dump(result_feed, json_file, indent=4, ensure_ascii=False)

print("Dictionary successfully written to output.json!")
