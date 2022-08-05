import prettyprint
import cfscrape
import requests
from bs4 import BeautifulSoup

scraper = cfscrape.create_scraper() #Bypasses cloudfare by utilizing nodejs
res = scraper.get("https://www.ge-tracker.com/item/old-school-bond").text #Scrapes data from ge-tracker
#print(res)

soup = BeautifulSoup(res, 'html.parser') #parses res.text as html
results = soup # changes soup to results for easier recall
#print(results)

buy=results.find_all(id="v_item_page") #Finds all data between <div id="v_item_page"> and </div>]
print(buy) #Prints all data from line above

