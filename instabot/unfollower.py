from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np
import time
import os

# Instagram user credentials:
instagram_username = os.environ['INSTA_USERNAME']
instagram_password = os.environ['INSTA_PASSWORD']

# All the X-Paths used: (Change if something stops working)
uname_input_path = '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input'
pass_input_path = '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input'
submit_btn_path = '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button'
followers_btn_path = '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a'
following_btn_path = '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a'
popup_path = '/html/body/div[5]/div/div/div[2]'
followers_count_path = '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span'
following_count_path = '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span'
account_name_link_path = '/div/div[1]/div[2]/div[1]/span/a'
unfollow_btn_path = '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button'
confirm_unfollow_btn_path = '/html/body/div[5]/div/div/div/div[3]/button[1]'

# All the css selectors used: (Fallbacks for when xpath didn't work)
ul_for_list_profiles = '.jSC57'

# All links:
instagram = 'https://www.instagram.com'
profile_page = f'https://www.instagram.com/{instagram_username}/'

# Selenium setup:
driver_path = os.environ['WEBDRIVER_PATH']
browser = webdriver.Firefox(executable_path=driver_path)

browser.get(instagram)
time.sleep(5)

username_input = browser.find_element_by_xpath(uname_input_path)
pass_input = browser.find_element_by_xpath(pass_input_path)
submit_button = browser.find_element_by_xpath(submit_btn_path)

# Log the user in:
username_input.send_keys(instagram_username)
pass_input.send_keys(instagram_password)
submit_button.click()
time.sleep(5)

# Followers and following estimation:
list_of_followers = []
list_of_following = []
browser.get(profile_page)
time.sleep(5)
number_followers = int(browser.find_element_by_xpath(followers_count_path).text)
number_following = int(browser.find_element_by_xpath(following_count_path).text)

# Go to followers after login:
browser.get(profile_page)
time.sleep(5)
followers_btn = browser.find_element_by_xpath(followers_btn_path)
followers_btn.click()
time.sleep(5)
for _ in range(10):
    popup = browser.find_element_by_xpath(popup_path)
    popup.send_keys(Keys.END)
    time.sleep(5)
ul_followers = browser.find_element_by_css_selector(ul_for_list_profiles)
list_followers = ul_followers.find_elements_by_tag_name('li')
for follower in list_followers:
    account_name_link = follower.find_element_by_tag_name('a')
    account_name = account_name_link.get_attribute('href')
    list_of_followers.append(account_name)

# Go to following after login:
browser.get(profile_page)
time.sleep(5)
following_btn = browser.find_element_by_xpath(following_btn_path)
following_btn.click()
time.sleep(5)
for _ in range(10):
    popup = browser.find_element_by_xpath(popup_path)
    popup.send_keys(Keys.END)
    time.sleep(5)
ul_following = browser.find_element_by_css_selector(ul_for_list_profiles)
list_following = ul_following.find_elements_by_tag_name('li')
for following in list_following:
    account_name_link = following.find_element_by_tag_name('a')
    account_name = account_name_link.get_attribute('href')
    list_of_following.append(account_name)

if len(list_of_following) != number_following:
    print('WARN: Looks like not all followings have been fetched, try increasing scrolling times.')
if len(list_of_followers) != number_followers:
    print('WARN: Looks like not all followers have been fetched, try increasing scrolling times.')

# Determine which users don't follow you back:
list_not_follow_back = np.setdiff1d(list_of_following, list_of_followers)

# Unfollow each and every one that doesn't follow back:
for name in list_not_follow_back:
    browser.get(name)
    time.sleep(5)
    unfollow_btn = browser.find_element_by_xpath(unfollow_btn_path)
    unfollow_btn.click()
    time.sleep(2)
    confirm_btn = browser.find_element_by_xpath(confirm_unfollow_btn_path)
    confirm_btn.click()
    time.sleep(2)
    print(f'Unfollowed: {name}')

if len(list_not_follow_back) == 0:
    print('No accounts to unfollow!')

time.sleep(10)
browser.quit()
