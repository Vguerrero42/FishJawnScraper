import bs4
import requests
import re
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import shelve
import os
import asyncio
import time

ua = UserAgent()

fishDataPath = '~/Projects/FishJawnDBData'


hrefStripper = re.compile(r'<li><a( class="mw-redirect")? href="/(.*?)"')

nameRegex = re.compile(r'(wiki/)(.*)')

#inital wiki page with list of marine life in NYC/Jersey area
fishWikiUrl = 'https://en.wikipedia.org/wiki/Marine_life_of_New_York%E2%80%93New_Jersey_Harbor_Estuary'

fishShelve = shelve.open('fishShelve')
fishData = {}

#function to grab html
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

#regex to grab links
linkList = hrefStripper.findall(str(fishes[0]))


#Navigate list, for each fish go to wiki page,grab first paragrahph ORdescription paragraph


def buildFishObj() :
  count = 0
  for link in linkList :
    description = ''
    currentPage = getPage(f'https://en.wikipedia.org/{link[1]}')
    name =  nameRegex.findall(link[1])[0][1]
    try:
      #look for h2 tag with id of description and grab that
      # description = currentPage.find(id="Description").find_parent(). find_next_sibling("p").text.strip()
      # print(description)
      description = currentPage.find(class_='mw-empty-elt').find_next_sibling("p").text.strip()      
    except:
      count += 1
      # print(f'ERROR COUNT {count}')
      # print(f'ERROR LINK {link[1]}')
      # after building fish "profiles" all data written to text FishShelve
    fishShelve[f'{name}'] =  description

    
buildFishObj()

for key in fishShelve.keys() :
  print(key,fishShelve[f'{key}'])


fishShelve.close()



# print(len(fishData.keys()))
# print(fishes[0])

# print(requests.get("http://en.wikipedia.org/wiki/American_shad").text)
#build object

# Builder/scraper finds top 10 fish in nyc area
# Scraper finds Fish page on wiki
# grabs [Locations:list,general stats(descriptions),]
# builds object fishes = {
# fish1 :{stuff},
# fish2:{stuff}
# }
# after building fish "profiles" all data written to text fishData.txt

