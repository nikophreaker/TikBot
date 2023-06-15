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

def detect_similar_objects(image_path, threshold_area=500, threshold_similarity=0.8):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to create a binary image
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > threshold_area]

    # Store the contours as arrays
    shape_arrays = []
    for contour in filtered_contours:
        contour_array = contour.squeeze(axis=1)  # Remove redundant axis
        shape_arrays.append(contour_array)

    # Draw the filtered contours and add text numbers
    for i, contour in enumerate(filtered_contours):
        cv2.drawContours(img, [contour], -1, (0, 255, 0), 2)
        # Find the center of the contour
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # Add text number at the center
        cv2.putText(img, str(i+1), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Show the image with the detected contours and text numbers
    cv2.imshow('Similar Objects', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return shape_arrays

def check_similarity(shape_arrays, threshold_similarity=0.25):
    similar_shapes = []
    for i in range(len(shape_arrays)):
        similar_indices = [i]
        for j in range(i + 1, len(shape_arrays)):
            if compare_shapes(shape_arrays[i], shape_arrays[j], threshold_similarity):
                similar_indices.append(j)
        if len(similar_indices) > 1:
            similar_shapes.append(similar_indices)
    return similar_shapes

def compare_shapes(shape1, shape2, threshold_similarity=0.25):
    similarity = cv2.matchShapes(shape1, shape2, cv2.CONTOURS_MATCH_I1, 0)
    return similarity < threshold_similarity

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
    # Detect similar objects based on shape and get the contour arrays
    contour_arrays = detect_similar_objects(captcha_image)

    # Check similarity between shape arrays
    similar_shapes = check_similarity(contour_arrays)

    # Write shape arrays to a file
    file_path = 'shape_arrays.txt'
    with open(file_path, 'w') as file:
        for i, shape_array in enumerate(contour_arrays):
            file.write(f"Shape {i+1}:\n")
            np.savetxt(file, shape_array, delimiter=',', fmt='%d')
            file.write('\n')

    # Write similar shapes to a file
    file_path = 'similar_shapes.txt'
    with open(file_path, 'w') as file:
        for indices in similar_shapes:
            file.write('Similar Shapes: ')
            for index in indices:
                file.write(f'Shape {index + 1} ')
            file.write('\n')

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