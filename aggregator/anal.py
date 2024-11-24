import json
from scraper import automate_links
from article_extractor import filter_html


with open("aggregate.json", "r", encoding="utf-8") as json_file:
    input = json.load(json_file)

with open("output.json", "r", encoding="utf-8") as json_file:
    output = json.load(json_file)

new_try = []
for art in input:
    if len([x for x in output if x["title"] == art["title"]]) == 0:
        new_try += [art]


res = automate_links(new_try)


result_feed = []
for article in res:
    article["html"] = filter_html(article["html"])
    if len(article["html"]) < 10000:
        print("TO LONF")
    result_feed += [article]

with open("untersuchen.json", "w", encoding="utf-8") as json_file:
    json.dump(result_feed, json_file, indent=4, ensure_ascii=False)
