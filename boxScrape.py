import requests
import sys
from bs4 import BeautifulSoup

f = open("box.txt","r")
http = f.read()
soup = BeautifulSoup(http)

rl = list()
for rs in soup.find_all("article",{"class":"nytc---cardbase---card"}):
	rl.append(rs.find('a')['href'].encode('utf-8'))

#bash script this shit
fo = ""
fo += "#!/bin/bash\n"
for r in rl:
	fo += "python scrape.py \"" + r + "\"\n"

f2 = open("recipePull.sh", "w+")
f2.write(fo)
f.close()
