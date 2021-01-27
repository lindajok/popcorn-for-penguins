"""
	Week1: Text mining from the web
	~Description~
	
	Building NLP Tools
	University of Helsinki
	22.1.2021

	Links:
	https://www.pluralsight.com/guides/extracting-data-html-beautifulsoup
	https://hamatti.org/posts/how-to-scrape-website-with-python-beautifulsoup/
	https://realpython.com/beautiful-soup-web-scraper-python/
	http://www.nltk.org/book/ch03.html#accessing-text-from-the-web-and-from-disk
"""

from urllib import request
from bs4 import BeautifulSoup

def main():
	# 1. choose an URL	
	url = "https://yle.fi"
        
	# 2. open URL and read it into a string
	html_doc = request.urlopen(url).read().decode('utf8')
        
	# 3. tokenize the string
	soup = BeautifulSoup(html_doc, "html.parser")

	# 4. filter the part we want form the string 
	# e.g. if we want the "most read news" section from yle.fi:	
	division = soup.find("div", attrs={"class": "StoryList__storyList___2DB4M StoryList__mostRead"})

	# 5. printing -->
	n = 1
	print() 
	print("Top 5 news in \"yle.fi\" right now:")
	print("=================================")
	print()

	# 6. remove the html tags
	# in this case, the headlines are inside tags "h3" :)        
	for heading in division.find_all('h3'):                                         
		row = f"{n}. {heading.text.strip()}"
		print(row)
		print("-"*len(row))
		n +=1
	print()


main()
