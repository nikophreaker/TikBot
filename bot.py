import numpy as np
from PIL import Image

import undetected_chromedriver as uc
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Path to the external text file containing account credentials
credentials_file = "credentials.txt"

# Instantiate the Chrome WebDriver
# driver = webdriver.Chrome()
# Add any desired options to the options object, if needed
# options = uc.ChromeOptions()
# driver = uc.Chrome(options=options)

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


# URL to navigate to after logging in
target_url = "https://www.tiktok.com/@nikxphreaker/video/6993669592551836930"

# Path to the external text file containing comment texts
comments_file = "comments.txt"

# Read account credentials from the text file
accounts = []
with open(credentials_file, "r") as file:
    for line in file:
        username, password = line.strip().split(",")
        account = {"username": username, "password": password}
        accounts.append(account)

# Read comment texts from the text file
comments = []
with open(comments_file, "r") as file:
    for line in file:
        comment = line.strip()
        comments.append(comment)

# Iterate over each account
for account in accounts:
    # Open TikTok website
    driver.get("https://www.tiktok.com/login/phone-or-email/email")

    # Wait for the page to load
    time.sleep(2)

    # Find the login button and click it
    # login_button = driver.find_element(By.LINK_TEXT, "Log in")
    # login_button.click()

    # Wait for the login page to load
    time.sleep(2)

    # Find the username input field and enter the username
    username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
    username_input.send_keys(account["username"])
    time.sleep(5)

    # Find the password input field and enter the password
    password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    password_input.send_keys(account["password"])
    time.sleep(5)

    # Press Enter to submit the login form
    password_input.send_keys(Keys.ENTER)

    print("sukses")

    # Wait for the login process to complete
    time.sleep(15)

    # Navigate to the target URL
    driver.get(target_url)

    # Interact with TikTok content
    #for _ in range(5):
    
    # Add likes to the post "div[id^='start-ads-']"
    like_button = driver.find_element(By.CSS_SELECTOR, "button[type-='like-icon']")
    like_button.click()
    time.sleep(1)
    # like_button = driver.find_element(By.CSS_SELECTOR, "button.like-button")
    # like_button.click()
    # time.sleep(1)

    # # Add comment to the post
    # # Select a random comment from the list
    # comment_text = random.choice(comments)
    # comment_input = driver.find_element(By.CSS_SELECTOR, "textarea.comment-input")
    # comment_input.send_keys(comment_text)
    # comment_input.send_keys(Keys.ENTER)
    # time.sleep(2)
        
    # Find a video element and extract the video URL
    #video_element = driver.find_element(By.CSS_SELECTOR, "a[href^='/v/']")
    #video_url = video_element.get_attribute("href")
    #print("Video URL:", video_url)

    # Move to the next video
    # driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_RIGHT)

    # Logout and clear cookies for the next account
    driver.delete_all_cookies()

# Close the browser
driver.quit()
