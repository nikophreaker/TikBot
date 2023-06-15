import cv2
import pytesseract
import pyautogui

import requests
import numpy as np
from pynput.mouse import Controller, Button

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Path to the external text file containing account credentials
credentials_file = "credentials.txt"

# Instantiate the Chrome WebDriver
driver = webdriver.Chrome()
# Add any desired options to the options object, if needed
# options = uc.ChromeOptions()
# driver = uc.Chrome(options=options)

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

    ###################################
    #solving captcha
    time.sleep(10)

    #get element img captcha
    image_element = driver.find_element(By.CSS_SELECTOR, "img[id='captcha-verify-image']")
    image_url = image_element.get_attribute("src")
    print(image_url)

    # Fetch the image data from the URL
    response = requests.get(image_url)
    image_data = response.content

    # Convert the image data to a NumPy array
    image_array = np.frombuffer(image_data, np.uint8)

    # Read the image using OpenCV's imread function
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Save the image with a specific filename
    filename = "output.jpg"  # Specify the desired filename
    cv2.imwrite(filename, image)

    # Load the captcha image
    captcha_image = cv2.imread('output.jpg')

    #===================================
    # Preprocess the image (apply any necessary image processing techniques)
    # Convert the image to grayscale
    gray = cv2.cvtColor(captcha_image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)

    # Perform morphological operations (optional)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh = cv2.erode(thresh, kernel, iterations=1)
    thresh = cv2.dilate(thresh, kernel, iterations=1)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate over the contours
    for contour in contours:
        # Calculate the area and aspect ratio of the contour
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h

        # Set thresholds for contour area and aspect ratio to filter out small and non-rectangular contours
        if area > 100 and aspect_ratio > 0.8 and aspect_ratio < 1.2:
            # Draw the contour on the original image
            cv2.drawContours(captcha_image, [contour], -1, (0, 255, 0), 2)

    # Display the image with the detected objects
    cv2.imshow('Detected Objects', captcha_image)
    cv2.waitKey(0)

    # Wait for the login process to complete
    time.sleep(60)


    # Navigate to the target URL
    # driver.get(target_url)

    # Interact with TikTok content
    #for _ in range(5):
    
    # # Add likes to the post
    # like_button = driver.find_element(By.CSS_SELECTOR, "span[data-e2e='like-icon']")
    # like_button.click()
    # time.sleep(1)
    # # like_button = driver.find_element(By.CSS_SELECTOR, "button.like-button")
    # # like_button.click()
    # # time.sleep(1)

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
