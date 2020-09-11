# Declare Dependencies 
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import os

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_all ():

    # Create a dictionary that can be imported to Mongo
    mars_dict = {}

    #NASA NEWS Scraping
    browser = init_browser()
    nasa_url = 'http://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    #Retrieve all elements that contain title and paragraph
    slide = soup.find('li', class_="slide")
    news_title = slide.find('div', class_='content_title').text
    news_paragraph = slide.find('div', class_='article_teaser_body').text 
    # Dictionary Entry: latest news' title and paragraph in dictionary
    mars_dict['news_title']= news_title
    mars_dict['news_paragraph']= news_paragraph
    
    # JPL Scparing  
    browser = init_browser()
    spaceimage_url = 'http://www.jpl.nasa.gov/spaceimages/?search=&category-Mars'
    browser.visit(spaceimage_url)

    # Go to Full Image by click the button
    browser.click_link_by_partial_text('FULL IMAGE')

    # Go to More Info by click the button
    browser.click_link_by_partial_text('more info')

    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Scrape the URL images with href info
    image_url = soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'
    # Dictionary Entry: JPL Mars Space Images - Featured Image
    mars_dict['featured_image_url'] = featured_image_url

    # Mars Facts Scraping
    browser = init_browser()
    facts_url = 'http://space-facts.com/mars/'
    browser.visit(facts_url)

    try:
        # Use Pandas to scrape the table containing facts about Mars Planet Profile
        mars_facts = pd.read_html(facts_url)[0]

    except BaseException:
        return None

    # Assign columns' name: Description and Mars 
    mars_facts.columns = ['Description', 'Mars']
    # Obtain the table with html file without index
    html_table = mars_facts.to_html(index=False)
    # Remove \n from the table
    html_table = html_table.replace('\n', '')
    # Dictionary Entry of table
    mars_dict['html_table'] = html_table

    #Mars Hemisphere Scparing
    browser = init_browser()
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    
    # Parse HTML with Beautiful Soup
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'html.parser')

    # Create a dictionary to store images' titles and links
    hemisphere_image_urls = []

    # Retrieve all elements that contain hemisphere information
    hemispheres = hemisphere_soup.find_all('div', class_='item')
    # Iterate through each image
    for hemisphere in hemispheres:
        # Find title with h3
        title = hemisphere.find("h3").text
        # Remove 'Enhanced' from the h3 title
        title = title.replace("Enhanced", "")
        # Collect image link name and browser visit each mars name link
        end_link_name = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link_name   
        browser.visit(image_link)
        # Then grab the 'Sample' full jpg image under class 'downloads' 
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        # Collect the image href for image_url
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    # Dictionary Entry of hemisphere images
    mars_dict['hemisphere_image'] = hemisphere_image_urls

    browser.quit()
    return mars_dict