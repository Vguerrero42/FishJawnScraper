import bs4
import requests
import re
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import shelve
import os


ua = UserAgent()

fishDataPath = '~/Projects/FishJawnDBData'

#inital wiki page with list of marine life in NYC/Jersey area
fishWikiUrl = 'https://en.wikipedia.org/wiki/Marine_life_of_New_York%E2%80%93New_Jersey_Harbor_Estuary'

#regex to grab links
hrefStripper = re.compile(r'<li><a( class="mw-redirect")? href="/(.*?)"')

#regex to grab fish name from links
nameRegex = re.compile(r'(wiki/)(.*)')


fishShelve = shelve.open('fishShelve')

#function to grab html and build soup object
def getPage(url) :
  header = {'User-Agent':str(ua.random)}
  res =  requests.get(url,headers=header)
  print(res.status_code,url)
  res.raise_for_status()
  soup = bs4.BeautifulSoup(res.text, 'html.parser')
  return soup

currentPage = getPage(fishWikiUrl)

#list of links under "fish"
fishes =  currentPage.select('#mw-content-text > div.mw-parser-output > ul:nth-child(13)')


linkList = hrefStripper.findall(str(fishes[0]))


#Navigate list, for each fish go to wiki page,grab first paragrahph OR description paragraph
def buildFishObj() :
  for link in linkList :
    description = ''
    currentPage = getPage(f'https://en.wikipedia.org/{link[1]}')
    name =  nameRegex.findall(link[1])[0][1]
    try:
      #look for h2 tag with id of description and grab that
      # description = currentPage.find(id="Description").find_parent(). find_next_sibling("p").text.strip()

      description = currentPage.find(class_='mw-empty-elt').find_next_sibling("p").text.strip()      
    except:
      #for debugging,initial searched for id of description but wiki articles are not uniform so changed to searching for first paragraph which in every wiki article is generally a quick description of subject.
      print(f'ERROR COUNT {count}')
      print(f'ERROR LINK {link[1]}')
      # after building fish "profiles" all data written to text FishShelve
    fishShelve[f'{name}'] =  description

    
buildFishObj()

#for debugging to ensure data written correctly.
for key in fishShelve.keys() :
  print(key,fishShelve[f'{key}'])


fishShelve.close()



# print(len(fishData.keys()))
# print(fishes[0])

#build object

# Builder/scraper finds top 10 fish in nyc area
# grabs [Locations:list,general stats(descriptions),]
# builds object fishes = {
# fish1 :{stuff},
# fish2:{stuff}
# }

