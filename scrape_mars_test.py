
# coding: utf-8
# ###############################################33333
################################################3
# In[16]:
# Mission to Mars

# Dependencies
# Import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
import requests
import time

import tweepy
import pymongo

import config
import pandas as pd

# # Step 1 - Scraping
# ###Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.


# Splinter set-up
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

# define a function
def scrape():
    browser = init_browser()
    # dictionary object for mongo
    nasa_news_mars = {}

# URL to be scraped
    NASA_url = "https://mars.nasa.gov/news/"
    browser.visit(NASA_url)

# create BeautifulSoup object and parse with 'html.parse'
    html = browser.html
    marsnews_soup = bs(html, 'html.parser')


# ### NASA Mars News
# news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
# 
# news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California --- the first interplanetary launch in history from America's West Coast."

# Latest news with title from NASA Mars News site - element1
    news_title = marsnews_soup.find_all('div', class_='content_title')
    print(news_title[0].text)
    print("test1")

# get paragraph start text-element2
    news_p = marsnews_soup.find_all('div', class_='article_teaser_body')
    print(news_p[0].text)
    print("test2")

# append element1 and element2 to dictionary nasa_news_mars
    nasa_news_mars['news_title'] = news_title[0].text
    nasa_news_mars['new_p'] = news_p[0].text

# ### JPL Mars Space Images - Featured Image

# featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'

    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    executable_path = {'executable_path': 'C:\ChromeSafe\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(featured_image_url)
    print("test3")

# browse pages with a latency
    time.sleep(2)

# click a button using click function
    fullimage_ele = browser.find_by_id("full_image")
    fullimage_ele.click()

    time.sleep(2)
    print("test4")

# click a button using click function
    image_info = browser.find_link_by_partial_text("more info")
    image_info.click()
    print("test5")

# create BeautifulSoup object and parse with 'html.parse'
    html = browser.html
    image_soup = bs(html, 'html.parser')
    print("test6")

# get the relative URL
    image_info_check = image_soup.find('figure', class_='lede').find('img')['src']
    image_info_check

# base url + relative url to get final url
    image_url = 'https://www.jpl.nasa.gov'
    featured_image_url_final = image_url + image_info_check
    featured_image_url_final
    print("test7")


# append final url to dictionary nasa_news_mars
    nasa_news_mars['featured_image_url_final'] = featured_image_url_final
    print("test8")

# ### Mars Weather

# # twitter regenerated keys
    consumer_key = "HZT0Bbm7t6jBM8y6encIAkFdi"
    consumer_secret ="uLzJTXZZ2dI1ZSyweZkjWaKXx224P23ik2P12FVcI76GgRhzbv"
    access_token ="1009237901073317888-Yv3kllm2ABnnU4q9ul2YvPEWobCpC8"
    access_token_secret= "amQNYDwe9ddEGL0lfoOXmZ7uGKAe2OJpSMHnCx1M5Q1Ze"


# from config import (consumer_key,
#                     consumer_secret,
#                     access_token,
#                     access_token_secret)

# Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


# twitter target user
    target_user = "@MarsWxReport"

# get latest tweets for news
    tweets_mars = api.user_timeline(target_user, count =100)
    Mars_weather = tweets_mars[0]['text']
    Mars_weather


# append latest tweets for news to dictionary nasa_news_mars
    nasa_news_mars['mars_weather'] = Mars_weather

# Mars Facts

# url Mars facts
    Mars_facts_url = 'https://space-facts.com/mars'

    df = pd.read_html(Mars_facts_url)[0]
    df.columns=['description', 'value']
    df.set_index('description', inplace =True)
# df

#df to html table 

    mars_profile_html =df.to_html()
#mars_profile_html

    mars_profile_html = mars_profile_html.replace('\n', '')
    nasa_news_mars['facts'] = mars_profile_html
    print("test9")

# # Mars Hemisphere

# scrape site to get image (large) and url 
featured_image_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(featured_image_url)
# soup object 
featured_image_url = browser.html
hemis_image_all = bs(featured_image_url, 'html.parser')


hemis_results = hemis_image_all.find('div', class_='collapsible results').find_all('div',class_='item')

# create empty list object
hemis_image_urls = [] 
each_hemis_image ={}
# Loop through hemisphere results
for each_image in hemis_results:
    
    title = each_image.find('div', class_='description').find('a', class_='itemLink product-item').h3.text
        # print(title)
        
        # Get each hemisphere image URL
    base_hemis_url = 'https://astrogeology.usgs.gov'

    each_hemis_image_url = base_hemis_url + each_image.find('a',class_='itemLink product-item')['href']
        #print(each_hemis_image_url)
        
    browser.visit(each_hemis_image_url)
    time.sleep(2)
    each_hemis_img_html = browser.html
    each_hem = bs(each_hemis_img_html, 'html.parser')
    full_image_url = each_hem.find('div',class_='downloads').a['href']
        ###print(full_image_url)
        
    each_hemis_image = {
            "title" : title,
            "image_url" : full_image_url
        }
    # print(each_hemis_image)

        # Append each hemisphere info to the list of all hemipheres  
    hemis_image_urls.append(each_hemis_image)


    nasa_news_mars["Hemisphere"] = hemis_image_urls


# hemis_image_urls

    print("Latest News!")
# return nasa_news_mars
      
browser.quit()