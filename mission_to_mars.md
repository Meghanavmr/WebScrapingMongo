

```python
# Dependencies
# Import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time

import tweepy
import pymongo

import config
```


```python
import pandas as pd
```

# Step 1 - Scraping
###Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.


```python
executable_path = {'executable_path': 'C:\ChromeSafe\chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
```


```python
NASA_url = "https://mars.nasa.gov/news/"
browser.visit(NASA_url)
```


```python
html = browser.html
marsnews_soup = bs(html, 'html.parser')
```

### NASA Mars News
news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"

news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California --- the first interplanetary launch in history from America's West Coast."


```python
news_title = marsnews_soup.find_all('div', class_='content_title')
print(news_title[0].text)
```

    Curiosity Surveys a Mystery Under Dusty Skies
    


```python
news_p = marsnews_soup.find_all('div', class_='article_teaser_body')
print(news_p[0].text)
```

    NASA's Curiosity rover surveyed its surroundings on Mars, producing a 360-degree panorama of its current location on Vera Rubin Ridge.
    

### JPL Mars Space Images - Featured Image


```python
# featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
```


```python
featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

executable_path = {'executable_path': 'C:\ChromeSafe\chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(featured_image_url)
```


```python
time.sleep(2)

fullimage_ele = browser.find_by_id("full_image")
fullimage_ele.click()
```


```python
time.sleep(2)

image_info = browser.find_link_by_partial_text("more info")
image_info.click()
```


```python
html = browser.html
image_soup = bs(html, 'html.parser')
```


```python
image_info_check = image_soup.find('figure', class_='lede').find('img')['src']
image_info_check
```




    '/spaceimages/images/largesize/PIA17172_hires.jpg'




```python
image_url = 'https://www.jpl.nasa.gov'
featured_image_url_final = image_url + image_info_check
featured_image_url_final
```




    'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA17172_hires.jpg'



### Mars Weather


```python
# # twitter regenerated keys
consumer_key = "HZT0Bbm7t6jBM8y6encIAkFdi"
consumer_secret ="uLzJTXZZ2dI1ZSyweZkjWaKXx224P23ik2P12FVcI76GgRhzbv"
access_token ="1009237901073317888-Yv3kllm2ABnnU4q9ul2YvPEWobCpC8"
access_token_secret= "amQNYDwe9ddEGL0lfoOXmZ7uGKAe2OJpSMHnCx1M5Q1Ze"
```


```python
# from config import (consumer_key,
#                     consumer_secret,
#                     access_token,
#                     access_token_secret)

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
```


```python
target_user = "@MarsWxReport"
```


```python
tweets_mars = api.user_timeline(target_user, count =100)
Mars_weather = tweets_mars[0]['text']
Mars_weather

```




    '@VeronicaMcG @NASAJPL Emmy wants his picture on the Cassini console in the SFOC'



Mars Facts


```python
Mars_facts_url = 'https://space-facts.com/mars'

df = pd.read_html(Mars_facts_url)[0]
df.columns=['description', 'value']
df.set_index('description', inplace =True)
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>value</th>
    </tr>
    <tr>
      <th>description</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Equatorial Diameter:</th>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>Polar Diameter:</th>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>Mass:</th>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>Moons:</th>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>Orbit Distance:</th>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>Orbit Period:</th>
      <td>687 days (1.9 years)</td>
    </tr>
    <tr>
      <th>Surface Temperature:</th>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>First Record:</th>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>Recorded By:</th>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
#df to html table 

mars_profile_html =df.to_html()
mars_profile_html

```




    '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>value</th>\n    </tr>\n    <tr>\n      <th>description</th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>Equatorial Diameter:</th>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <th>Polar Diameter:</th>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <th>Mass:</th>\n      <td>6.42 x 10^23 kg (10.7% Earth)</td>\n    </tr>\n    <tr>\n      <th>Moons:</th>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <th>Orbit Distance:</th>\n      <td>227,943,824 km (1.52 AU)</td>\n    </tr>\n    <tr>\n      <th>Orbit Period:</th>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <th>Surface Temperature:</th>\n      <td>-153 to 20 °C</td>\n    </tr>\n    <tr>\n      <th>First Record:</th>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <th>Recorded By:</th>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>'



# Mars Hemisphere


```python
# scrape site to get image (large) and url 
featured_image_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(featured_image_url)

featured_image_url = browser.html
hemis_image_all = bs(featured_image_url, 'html.parser')
```


```python
hemis_results = hemis_image_all.find('div', class_='collapsible results').find_all('div',class_='item')
```


```python
hemis_image_urls = [] 

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
    print(each_hemis_image)
    # Append each hemisphere info to the list of all hemipheres  
    hemis_image_urls.append(each_hemis_image)




```

    {'title': 'Cerberus Hemisphere Enhanced', 'image_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'}
    {'title': 'Schiaparelli Hemisphere Enhanced', 'image_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'}
    {'title': 'Syrtis Major Hemisphere Enhanced', 'image_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}
    {'title': 'Valles Marineris Hemisphere Enhanced', 'image_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}
    


```python
hemis_image_urls
```




    [{'image_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg',
      'title': 'Cerberus Hemisphere Enhanced'},
     {'image_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg',
      'title': 'Schiaparelli Hemisphere Enhanced'},
     {'image_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg',
      'title': 'Syrtis Major Hemisphere Enhanced'},
     {'image_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg',
      'title': 'Valles Marineris Hemisphere Enhanced'}]


