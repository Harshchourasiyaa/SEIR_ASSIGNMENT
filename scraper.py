import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

link = sys.argv[1]

headers = {
    "User-Agent": "Mozilla/5.0"
}

pageresponse = requests.get(link,headers=headers)
parsedhtml = BeautifulSoup(pageresponse.text, "html.parser")

print("\n**--TITLE--**")
print(parsedhtml.title.text.strip())

print("\n**--BODY TEXT--**")
print(parsedhtml.body.get_text(separator="\n",strip=True)[:1500])

print("\n**--LINKS--**")
set_links = set()
for anchortag in parsedhtml.find_all("a"):
    weburl = anchortag.get("href")
    if weburl:
        fullurl = urljoin(link,weburl)
        if fullurl.startswith("http") and "#" not in fullurl:
            set_links.add(fullurl)

for url in set_links:
    print(url)

