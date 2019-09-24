import urllib.request
import urllib.parse

google = urllib.request.urlopen('http://google.com')
google = google.read()
print(google[:200])

url = 'http://google.com?q='
url_with_query = url + urllib.parse.quote_plus('python web scraping')

web_search = urllib.request.urlopen(url_with_query)
web_search = web_search.read()
print(web_search[:200])
