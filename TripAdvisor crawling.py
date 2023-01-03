from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

import argparse

parser = argparse.ArgumentParser(description='input Review starting number')

parser.add_argument('--num', required=True, help='review starting number')
args= parser.parse_args()
print(args.num)

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--disable-web-security")
options.add_argument("--disable-site-isolation-trials")

driver = webdriver.Chrome('ChromeDriver file route', options= options)

review_num =args.num

# Get review URL from TripAdvisor website
# Attraction point url looks like: https://www.tripadvisor.com/Attraction_Review-g186338-d187555-Reviews-or10000The_British_Museum-London_England.html
# In 10000 position you can put your starting number with argparse

#Example : The British Museum 
url = 'https://www.tripadvisor.com/Attraction_Review-g186338-d187555-Reviews-or'+review_num+'The_British_Museum-London_England.html'

driver.get(url)


comment_list = []
id_list =[]
rank_list = []
title_list =[]
loc_list =[]
likes_list =[]
date_list=[]

page =0

while True :
    # Press every more buttons
    try :
        more_btns = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located([By.CSS_SELECTOR, 'div.LbPSX div.lszDU button span']))
    #more_btns = driver.find_elements_by_css_selector('div.LbPSX div.lszDU button span')
    
        for btn in more_btns:
            try : 
                btn.click() # 버튼이 따로 없어도 button 칸이 있어서 누를 수 있는 버튼만 누르도록 지시
            except :
                continue
    except:
        continue

    time.sleep(2)


    # Reviewer ID      
    id_tags = driver.find_elements_by_css_selector('div.LbPSX div.zpDvc span a')

    for id in id_tags :
        id_list.append(id.text)


    # Location - if there are no location it represents as "~ contibute"
    loc_tags = driver.find_elements_by_css_selector('div.LbPSX div.zpDvc div span:nth-child(1)')

    for loc in loc_tags :
        loc_list.append(loc.text)

    # Likes on the review  
    like_tags = driver.find_elements_by_css_selector('div.mwPje.f.M.k > div:nth-child(2) > button > span > span')

    for like in like_tags :
        likes_list.append(like.text)

    # Rank on the review
    rank_tag = driver.find_elements_by_css_selector('div.LbPSX > div > span > div > div:nth-child(2) > svg')

    for rank in rank_tag :
        rank_list.append(rank.get_attribute('aria-label')[0:3])

    # Review title   
    title_tags = driver.find_elements_by_css_selector('div.LbPSX span div div a span')

    for title in title_tags :
        title_list.append(title.text)
        
        
    # Review texts

    comment_tags = driver.find_elements_by_css_selector('div.LbPSX div._T.FKffI  div.fIrGe._T.bgMZj div')

    for comment in comment_tags :
        comment_list.append(comment.text)
        
    # review date
    date_tags = driver.find_elements_by_css_selector('div.LbPSX span div div.TreSq div.biGQs._P.pZUbB.ncFvv.osNWb')

    for date in date_tags :
        date_list.append(date.text[8:])
    
    time.sleep(3)
    
    # Next page
    
    try :
        next_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located([By.CSS_SELECTOR, 'div.xkSty > div > a']))
        next_btn.click()
        page +=1
        print(page)
        if page ==200 : # if you want to collect more pages, you can increase the number 
            print('2000 reviews collected')
            break
    except :
        print('finish')
        break
    
    time.sleep(1)

driver.quit()    
    
import pandas as pd
df = pd.DataFrame((zip(id_list, loc_list, date_list, title_list, comment_list, rank_list, likes_list)), columns=['ID', 'location', 'date', 'title', 'review', 'rank', 'likes'])
# print number of collected reviews
print(len(df))
df.to_csv('./_'+args.num+'_review.csv')