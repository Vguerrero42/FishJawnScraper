import bs4
import requests
import re
from fake_useragent import UserAgent
import os
import json


ua = UserAgent()

fishDataPath = '/home/victor/Projects/FishJawnDBData'


#inital wiki page with list of marine life in NYC/Jersey area
fishWikiUrl = 'https://en.wikipedia.org/wiki/Marine_life_of_New_York%E2%80%93New_Jersey_Harbor_Estuary'

#regex to grab links
hrefStripper = re.compile(r'<li><a( class="mw-redirect")? href="/(.*?)"')

#regex to grab fish name from links
nameRegex = re.compile(r'(wiki/)(.*)')


fishData = {}

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

#cleaned list of links without html
linkList = hrefStripper.findall(str(fishes[0]))


#Navigate list, for each fish go to wiki page,grab first paragrahph OR description paragraph
def buildFishObj() :
  for link in linkList :
    description = ''
    currentPage = getPage(f'https://en.wikipedia.org/{link[1]}')
    name =  nameRegex.findall(link[1])[0][1]
    try:
      #look for h2 tag with id of description and grab that then find paragraph under it
      # description = currentPage.find(id="Description").find_parent(). find_next_sibling("p").text.strip()

      #this just grabs first paragraph 
      description = currentPage.find(class_='mw-empty-elt').find_next_sibling("p").text.strip()      
    except:
      #for debugging,initially searched for id of description but wiki articles are not uniform so changed to searching for first paragraph which in every wiki article is generally a quick description of subject.
      print(f'ERROR COUNT {count}')
      print(f'ERROR LINK {link[1]}')
    
    # after building fish "profiles" all data written to text fishData object
    fishData[f'{name}'] =  description


    
buildFishObj()

#for debugging to ensure data written correctly.
for key in fishData.keys() :
  print(key,fishData[f'{key}'])

#writing data to file to be used for DB seed
with open(f'{fishDataPath}/fishData.txt','a') as path :
  json.dump(fishData,path)





