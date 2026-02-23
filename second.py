import sys
import requests
from collections import Counter
from bs4 import BeautifulSoup

def pagetext(link):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    pageresponse = requests.get(link, headers = headers)
    # print(pageresponse)
    parsedhtml = BeautifulSoup(pageresponse.text, "html.parser")
    return parsedhtml.get_text(separator=" ",strip=True).lower()

def wordtohash(word):
    base = 53
    modulo = 2**64
    hashvalue = 0
    times = 1

    for letter in word:
        hashvalue = (hashvalue + ord(letter)*times)%modulo
        times = (times*base)%modulo

    return hashvalue

def textosimhash(text):
    cleanedtext = ""
    for ch in text:
        if ch.isalnum() or ch == " ":
            cleanedtext += ch


    cleanedtext = cleanedtext.lower()
    wordlist = cleanedtext.split()
    wordfreq = Counter(wordlist)
    bitsvector = [0]*64

    for word, count in wordfreq.items():
        hash = wordtohash(word)

        binary = bin(hash)[2:]
        numofzeroes = 64-len(binary)
        binary = "0"*numofzeroes + binary

        for i in range(64):
            if binary[i] == "1":
                bitsvector[i] += count
            else:
                bitsvector[i] -= count

    simhash = ""
    for bit in bitsvector:
        if bit>=0:
            simhash += "1"
        else:
            simhash += "0"

    return simhash

def numof_samebits(simh1,simh2):
    samebits = 0
    for i in range(64):
        if simh1[i] == simh2[i]:
            samebits += 1
    return samebits

link1 = sys.argv[1]
link2 = sys.argv[2]

content1 = pagetext(link1)
content2 = pagetext(link2)

simh1 = textosimhash(content1)
simh2 = textosimhash(content2)

print("Simhash of Link1:")
print(simh1)
print("\nSimhash of Link2:")
print(simh2)

print("\nNumber of Same bits:")
print(numof_samebits(simh1,simh2))


