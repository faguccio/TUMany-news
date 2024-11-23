from aggregator import retrieve_feed
from scraper import automate_links
from article_extractor import filter_html
import json

# Each article contain important metadata
articles_feed = retrieve_feed()


# Extract HTML from each article
articles_feed = automate_links(articles_feed)

for article in articles_feed:
    article["html"] = filter_html(article["html"])


with open("output.json", "w", encoding="utf-8") as json_file:
    json.dump(articles_feed, json_file, indent=4, ensure_ascii=False)

print("Dictionary successfully written to output.json!")
