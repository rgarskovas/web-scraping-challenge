# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import os
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)


def mars_news():
    
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrap page to soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Find the relevant title and the teaser text
    full_news = soup.find("li", class_="slide")
    news_title = full_news.find("div", class_="content_title").get_text()
    news_teaser = soup.find("div", class_="article_teaser_body").get_text()

    return news_title, news_teaser

def mars_feat_image():
    # connect to browser, enable list, and set to sleep
    browser = init_browser()
    mars_image = {}

    time.sleep(1)

    # add url and base url
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_url = "https://www.jpl.nasa.gov/"
    browser.visit(url)

    # connect to html
    html = browser.html
    soup = bs(html, "html.parser")

    # split the url into full
    full_url = soup.find_all('article')[0]["style"]
    relative_image_path = full_url.split("('", 1)[1].split("')")[0]


    mars_image = base_url + relative_image_path

    return mars_image

def mars_facts():
    
    # get the space facts from online and convert to html
    df = pd.read_html('http://space-facts.com/mars/')[0]
    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)
    html_table = df.to_html()
    html_table.replace('\n', '')

    return html_table

def mars_images():

    # visit the site to find hemisphere data
    browser = init_browser()
    time.sleep(1)
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
  
    # find all h3 and establish lists
    hemisphere_names = soup.find_all('h3')
    name_list = []
    mars_hem_list = []
           
    base_url = "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/"

    # build the dictionary based on titles and names
    for h in hemisphere_names:
        title = h.text.strip()
        name_list.append(title)
        url = base_url + title + ".tif/full.jpg"
        url = url.replace('Hemisphere ', '')
        url = url.replace(" ", "_")
        mars_hem_list.append({'Name':title, 'URL': url})
    

    return mars_hem_list

def scrape():
   # browser = init_browser()
    
    news_title, news_teaser = mars_news()

    # run all functions
    mars_master_data = {
        "news_title": news_title,
        "mars_headlines": news_teaser,
        "mars_image": mars_feat_image(),
        "table_dict": mars_facts(),
        "mars_hem_list": mars_images(),
    }     

    return mars_master_data

if __name__ == "__main__":
    print(scrape())