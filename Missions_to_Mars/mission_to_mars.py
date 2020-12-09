#!/usr/bin/env python
# coding: utf-8

# ### Nasa Mars News

# In[152]:


#Import dependencies needed
import pandas as pd
import os
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

# In[143]:
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():

    response = requests.get('https://mars.nasa.gov/news/')


    # In[144]:


    html = response.text
    soup = bs(html, 'html.parser')
    #soup


    # In[145]:


    news_titles = soup.find_all('div', class_='content_title')
    news_titles


    # In[146]:


    title = news_titles[0].text.strip('\n')


    # In[147]:


    news_p = soup.find('div', {'class': 'rollover_description_inner'}).text.strip('\n')
    news_p


    # In[149]:

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    #browser.quit()


    # # ## JPL Mars Space Images - Featured Image

    # In[150]:





    # In[164]:


    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    browser.click_link_by_partial_text('FULL IMAGE') 
    time.sleep(5) 
    browser.click_link_by_partial_text('more info') 
    html = browser.html
    soup = bs(html,'html.parser')


    # In[159]:


    result = soup.find('figure',{'class':'lede'}).a['href']
    result


    # In[165]:


    jpl_base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = jpl_base_url + result
    print(featured_image_url)


    # ### Mars Facts

    # In[166]:


    mars_facts_url = 'https://space-facts.com/mars/'


    # In[167]:


    facts_df = pd.read_html(mars_facts_url)
    facts_df


    # In[169]:


    final_facts_df = facts_df[0]
    final_facts_df


    # In[170]:


    final_facts_df.columns = ['Facts', 'Values']
    final_facts_df


    # In[171]:


    final_facts_df.set_index ('Facts', inplace=True)


    # In[172]:


    facts_html = final_facts_df.to_html(index=False)


    # ### Mars Hemisphere

    # In[173]:


    hemisphere_img_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    # In[174]:


    browser.visit(hemisphere_img_url)


    # In[175]:


    html_h = browser.html
    soup_h = bs(html_h,'html.parser')


    # In[176]:


    img_1 = soup_h.find_all('div', class_='item')
    img_1


    # In[177]:


    img_list = []
    for img in img_1:
        img_url = img.find('a')['href']
        title = img.find('div', class_='description').find('a').find('h3').text
        final_url = 'https://astrogeology.usgs.gov' + img_url
        browser.visit(final_url)
        html_h = browser.html
        soup_h = bs(html_h,'html.parser')
        final_img = soup_h.find('div', class_='downloads').find('ul').find('li').find('a')['href']
        img_list.append({'title': title, 'img_url': final_img})
    img_list

    scrape_data = {
        'news_title': title, 
        'paragraph': news_p,
        'featured_img': featured_image_url,
        'facts': facts_html,
        'images': img_list
    }

    return scrape_data
    # In[ ]:




