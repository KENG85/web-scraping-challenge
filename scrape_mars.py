#!/usr/bin/env python
# coding: utf-8


#!pip install splinter
#!pip install IPython
from splinter import Browser
from bs4 import BeautifulSoup as bs, NavigableString as ns
from IPython.display import display_html
import pandas as pd
import requests
import time
import re
from sys import platform
from urllib.parse import urlsplit
from bs4 import BeautifulSoup 
import pandas as pd
from pprint import pprint

def scrape():

    #   def init_Browser():
    #   # @NOTE: Replace the path with your actual path to the chromedriver
    #   executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    #   return Browser("chrome", **executable_path, headless=False)
    browser = Browser('chrome')
    mars = {}
    
    url = "https://mars.nasa.gov/news/"

    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars["Title"] = soup.find("div", class_="content_title").get_text()
    mars["Description"] = soup.find("div", class_="rollover_description_inner").get_text()
    browser.quit()
    browser = Browser("chrome")
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    browser.find_by_id("full_image").click()
    time.sleep(2)

    browser.links.find_by_partial_text("more info").click()
   
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    link = soup.find("figure", class_="lede")
    featured_image = "https://www.jpl.nasa.gov" + link.a.img["src"]

    mars["Featured_image"] = featured_image
    
    browser.quit()
    browser = Browser("chrome")

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(1)


    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    weather = re.compile(r'sol')
    mars["Weather"] = soup.find('span', text=weather).text
    
    browser.quit()
    browser = Browser("chrome")
    url = "https://space-facts.com/mars/"

    df = pd.read_html(url)[0]
    df = df.to_html()
    mars["Facts"] = df

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    title = soup.find_all('h3')
    print(len(link))
    #print(link[0]['href'])

    browser.quit()
    browser = Browser("chrome")
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    link = browser.find_by_css("a.product-item h3")
    hemisphere_img = []
    #image_url = {}

    for x in range(len(link)):   
        image_url = {}
        browser.find_by_css("a.product-item h3")[x].click()
        #link = soup.find_all('a', class_="itemLink product-item")
        sample = browser.find_link_by_text('Sample').first
        #hemisphere_img["Img_url"] = sample['href']
    
        image_url["Title"] =  browser.find_by_css("h2.title").text
        image_url["Img_url"] = sample['href']
        hemisphere_img.append(image_url)
        browser.back()


    mars["Hemisphere"] = hemisphere_img
    return mars

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape())

