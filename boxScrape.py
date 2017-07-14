import requests
import sys
from bs4 import BeautifulSoup

#if len(sys.argv) != 2:
print "\n\nThank you for using Desync's Wonderous Recipe Box Scraper"
print "requeires requests and beautifulsoup4"
print ">> pip install requests"
print ">> pip install beautifulsoup4"
print "Usage:   in terminal type >> python boxScrape.py \"<NYT cooking recipe box url>\""
print "Outputs a bash script to automate box translation"
#	sys.exit()
#else: 
#	http = str(sys.argv[1])

http = "https://cooking.nytimes.com/74076200?action=click&module=nav&region=your%20recipe%20box&pgType=recipe-page"  ## debug code

try:
	recipe_web_raw = requests.get(http)
except:
	print "\nFatal error:  Web page not retrieved, check url\n"
	sys.exit()
recipe_html = recipe_web_raw.content

soup = BeautifulSoup(recipe_html, "html.parser")
print soup

rl = list()
for rs in soup.find_all("div",{"class":"nytc---cardbase---imageWrap"}):
	rl.append(rs)
	#rl.append(rs.find('a')['href'])
print "link list"
for r in rl:
	print r
	
