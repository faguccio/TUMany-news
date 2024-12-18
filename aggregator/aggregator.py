import requests


def fetch_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


def retrieve_feed(rss_url):
    print("Retrieving news from RSS feed")
    json_data = fetch_json(rss_url)

    aggregate = []

    if json_data:
        if "items" in json_data:
            for item in json_data["items"]:
                aggregate += [{
                    "title": item.get('title', 'No title'),
                    "description": item.get('content_text', 'No description'),
                    "image": item.get('image', 'No image'),
                    "date": item.get('date_published', 'No date'),
                    "url": item.get('url'),
                }]

    print(f"Retrieved {len(aggregate)} articles")
    return aggregate
