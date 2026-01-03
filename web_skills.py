import webbrowser
import urllib.parse

def open_url(url):
    """Opens a URL in the default browser."""
    print(f"Opening URL: {url}")
    webbrowser.open(url)

def search_google(query):
    """Searches Google for the given query."""
    print(f"Searching Google for: {query}")
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    webbrowser.open(url)
