from bs4 import BeautifulSoup


def filter_html(input_html):
    # Read the HTML file
    if (type(input_html) is dict):
        print(input_html.keys())
    soup = BeautifulSoup(input_html, 'html.parser')

    def filter_element(element):
        """
        Recursively clean an element to retain only <h1>-<h6> and <p> tags.
        """
        children = list(element.children)

        res = []

        for child in children:
            if child.name is None:
                continue
            if (child.name.startswith('h') and child.name[1:].isdigit()) or child.name == 'p':
                # base case, return the content
                child.attrs = {}
                res += [child]
            else:
                # it is a tag, but not the base case, recurse on it and save result
                res += filter_element(child)

        return res

    if soup.body:
        return str(filter_element(soup.body))
    else:
        # Fallback in case there's no <body>
        return str(filter_element(soup))
