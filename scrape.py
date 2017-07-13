import requests
import sys
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
	print "\n\nThank you for using Desync's Wonderous Scraper"
	print "requires requests and beautifulsoup4"
	print ">> pip install requests"
	print ">> pip install beautifulsoup4"
	print "Usage:   in terminal type >> python scrape.py \"<Nyt cooking recipe address>\""
	print "Define output type in program, default is .txt"
	http = ""
	print len(sys.argv)
	print str(sys.argv[1])
	sys.exit()
else:
	http = str(sys.argv[1])
	
output = 1 #1 for .tex 2 for .txt

try:
	recipe_web_raw = requests.get(http)
except:
	print "\nFatal error:  Web page not retrieved, check url\n"
	sys.exit()
if recipe_web_raw.status_code != 200: #something went wrong
		print "\nFatal Error:  Web page not retrieved, check url\n"
		sys.exit()
recipe_html = recipe_web_raw.content

soup = BeautifulSoup(recipe_html, "html.parser")

#title
title = soup.find('h1')
title = title.get_text().encode('utf-8')
title = title.strip()

#description
try:
	description = soup.find("div", {"class":"topnote"})
	if description is not None:
		description = description.get_text().encode('utf-8')
except:
	description = ""

#need to format to one line
try:
	recipeYield = soup.find(itemprop="recipeYield")
	recipeYield = recipeYield.get_text().encode('utf-8')
except:
	recipeYield = ""

#need to format out PT and do nice minutes / hours
#cookTime = soup.find(itemprop="cookTime")
try:
	cookTime = soup.find("meta", {"itemprop":"cookTime"})['content']

#formatting string
	cookTime_Final = " minutes"
	for c in reversed(cookTime):
		if c == 'H':
			cookTime_Final = '%s%s' % (' hours ', cookTime_Final)
		elif c =='M' or c =='T' or c == 'P':
			pass
		else:
			cookTime_Final = '{}{}'.format(c, cookTime_Final)
	cookTime_Final = cookTime_Final.encode('utf-8')
except:
	cookTime_Final = '    '


quantities = soup.find_all("span", {"class":"quantity"})
for q in range(len(quantities)):
	quantities[q] = quantities[q].get_text().encode('utf-8')
	quantities[q] = quantities[q].strip()

#need to place on one line
ingredients = soup.find_all("span", {"class":"ingredient-name"})
ingredients_final = list()
for ing in ingredients:
	ingredients_final.append(ing.get_text().encode('utf-8'))
for i in range(len(ingredients_final)):
	ingredients_final[i] = ingredients_final[i].replace("tablespoon", "tbsp")
	ingredients_final[i] = ingredients_final[i].replace("teaspoon","tsp")
	ingredients_final[i] = ingredients_final[i].strip()

#combine quantities and ingredients
ing = list()
for i in range(len(ingredients_final)):
	ing.append('{} {}'.format(quantities[i], ingredients_final[i]))



steps_text = list()
for steps in soup.find_all(itemprop="recipeInstructions"):
	for s in steps.find_all('li'):
		steps_text.append(s.text)
for s in range(len(steps_text)):
	steps_text[s] = steps_text[s].encode('utf-8')


if output ==1:  #.tex
	f_o = ""
	f_o = f_o + '\\begin{{recipe}}{{{}}}{{{}}}{{{}}}\n'.format(title, recipeYield, cookTime_Final)
	f_o = f_o + '\\freeform{}\n'.format(description)
	f_o = f_o + '\\freeform\\hrulefill\n'
	for x in ing:
		f_o = f_o + '\\Ingredient{{{}}}\n'.format(x)
	for y in steps_text:
		f_o = f_o + '{}\n'.format(y)
	f_o = f_o + '\\end{recipe}'
	#write to file
	f = open("{}.tex".format(title.replace(" ", "")), "w+")
	f.write(f_o)
	f.close

else:
	f_o = ""
	f_o += title + "\n"
	f_o += recipeYield + "\n"
	f_o += cookTime_Final + "\n\n\n"
	for x in ing:
		f_o += x+"\n"
	f_o += "\n\n"
	for y in steps_text:
		f_o += y + "\n"
	print f_o
	#write
	f = open("{}.txt".format(title.replace(" ", "")), "w+")
	f.write(f_o)
	f.close
