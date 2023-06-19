import numpy as np
from PIL import Image
import pandas as pd

from pynput.mouse import Controller, Button
import random
import undetected_chromedriver as uc
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Path to the external text file containing account credentials
credentials_file = "credentials.txt"

# Specify the file path of the Excel file
excel_file = 'AKUN GMAIL.xlsx'

# Instantiate the Chrome WebDriver
# driver = webdriver.Chrome()
# Add any desired options to the options object, if needed
# options = uc.ChromeOptions()
# driver = uc.Chrome(options=options)

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# Add the --mute-audio flag
options.add_argument("--mute-audio")

# options.add_argument("--headless")

# Set the proxy IP address and port
proxy_ip = '199.102.105.242'
proxy_port = '4145'

# Configure the Selenium WebDriver to use the proxy server
proxy_options = {
    'proxy': {
        'proxyType': 'MANUAL',
        'httpProxy': f'{proxy_ip}:{proxy_port}',
        'sslProxy': f'{proxy_ip}:{proxy_port}'
    }
}

# options.add_argument('user_agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        proxy_options=proxy_options
        )

# URL to navigate to after logging in
target_url = "https://www.tiktok.com/@nikxphreaker/video/6993669592551836930"

# Path to the external text file containing comment texts
comments_file = "comments.txt"

# Read account credentials from the excel file
accounts = []

# Specify the sheet name (if it's not the default sheet)
sheet_name = 'MARSHA'

# Specify the columns and rows you want to extract
columns = ['Gmail', 'Password.2']  # Replace with your desired column names
start_row = 25  # Replace with the starting row index
end_row = 51  # Replace with the ending row index

# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file, sheet_name=sheet_name)

selected_data = df.loc[start_row:end_row, [columns[0], columns[1]]]
data = pd.DataFrame(selected_data)

# Drop rows with NaN values
data = data.dropna()

# Convert the DataFrame to a list of dictionaries
result = data.to_dict(orient='records')

# Separate the values per row with a comma
for item in result:
    # Skip even numbers
    if item[columns[0]] == str('nan') or item[columns[1]] == str('nan') :
        continue
    account = {"username": item[columns[0]], "password": item[columns[1]]}
    accounts.append(account)   
    # item[columns[0]] = str(item[columns[0]])
    # item[columns[1]] = str(item[columns[1]])
    # item[columns[0]] = ', '.join(item[columns[0]].splitlines())
    # item[columns[1]] = ', '.join(item[columns[1]].splitlines())

# Print the result (list of dictionaries)
# print(accounts)

# with open(credentials_file, "r") as file:
#     for line in file:
#         username, password = line.strip().split(",")
#         account = {"username": username, "password": password}
#         accounts.append(account)

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

    # ############################################
    # #### Resolve captcha
    # ############################################
    # import cv2
    # import numpy as np
    # import requests

    # # Navigate to the target URL
    # image_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[id='captcha-verify-image']")))

    # #get element img captcha
    # image_url = image_element.get_attribute("src")
    # print(image_url)

    # # Fetch the image data from the URL
    # response = requests.get(image_url)
    # image_data = response.content

    # # Convert the image data to a NumPy array
    # image_array = np.frombuffer(image_data, np.uint8)

    # # Read the image using OpenCV's imread function
    # image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # # Save the image with a specific filename
    # filename = "output.jpg"  # Specify the desired filename
    # cv2.imwrite(filename, image)

    # def detect_similar_objects(image_path, threshold_area=500, threshold_similarity=0.8):
    #     # Load the image
    #     img = cv2.imread(image_path)

    #     # Convert the image to grayscale
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #     # Apply adaptive thresholding to create a binary image
    #     _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    #     # Find contours in the binary image
    #     contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #     # Filter contours based on area
    #     filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > threshold_area]

    #     # Store the contours as arrays
    #     shape_arrays = []
    #     for contour in filtered_contours:
    #         contour_array = contour.squeeze(axis=1)  # Remove redundant axis
    #         shape_arrays.append(contour_array)

    #     # Draw the filtered contours and add text numbers
    #     for i, contour in enumerate(filtered_contours):
    #         cv2.drawContours(img, [contour], -1, (0, 255, 0), 2)
    #         # Find the center of the contour
    #         M = cv2.moments(contour)
    #         cX = int(M["m10"] / M["m00"])
    #         cY = int(M["m01"] / M["m00"])
    #         # Add text number at the center
    #         cv2.putText(img, str(i+1), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    #     # Show the image with the detected contours and text numbers
    #     cv2.imshow('Similar Objects', img)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    #     return shape_arrays

    # def check_similarity(shape_arrays, threshold_similarity=0.25):
    #     similar_shapes = []
    #     for i in range(len(shape_arrays)):
    #         similar_indices = [i]
    #         for j in range(i + 1, len(shape_arrays)):
    #             if compare_shapes(shape_arrays[i], shape_arrays[j], threshold_similarity):
    #                 similar_indices.append(j)
    #         if len(similar_indices) > 1:
    #             similar_shapes.append(similar_indices)
    #     return similar_shapes

    # def compare_shapes(shape1, shape2, threshold_similarity=0.25):
    #     similarity = cv2.matchShapes(shape1, shape2, cv2.CONTOURS_MATCH_I1, 0)
    #     return similarity < threshold_similarity

    # # Set the path to your image
    # image_path = 'output.jpg'

    # # Detect similar objects based on shape and get the contour arrays
    # contour_arrays = detect_similar_objects(image_path)

    # # Check similarity between shape arrays
    # similar_shapes = check_similarity(contour_arrays)

    # # Write shape arrays to a file
    # file_path = 'shape_arrays.txt'
    # with open(file_path, 'w') as file:
    #     for i, shape_array in enumerate(contour_arrays):
    #         file.write(f"Shape {i+1}:\n")
    #         np.savetxt(file, shape_array, delimiter=',', fmt='%d')
    #         file.write('\n')

    # # Write similar shapes to a file
    # file_path = 'similar_shapes.txt'
    # with open(file_path, 'w') as file:
    #     for indices in similar_shapes:
    #         file.write('Similar Shapes: ')
    #         for index in indices:
    #             file.write(f'Shape {index + 1} ')
    #         file.write('\n')

    # # Initialize the mouse controller
    # mouse = Controller()

    # # Simulate touch on similar shapes
    # def simulate_touch(similar_shapes):
    #     for shape_indices in similar_shapes:
    #         # Get the contour of the first shape
    #         contour = contour_arrays[shape_indices[0]]

    #         # Find the center of the contour
    #         M = cv2.moments(contour)
    #         cX = int(M["m10"] / M["m00"])
    #         cY = int(M["m01"] / M["m00"])

    #         # Simulate left button click at the center position
    #         mouse.position = (cX, cY)
    #         mouse.click(Button.left)
    #         time.sleep(2)

    # # Check similarity between shape arrays
    # similar_shapes = check_similarity(contour_arrays)

    # # Simulate touch on similar shapes
    # simulate_touch(similar_shapes)

    # Wait for the login process to complete
    time.sleep(15)

    # Navigate to the target URL
    driver.get(target_url)
    
    time.sleep(5)
    

    ############################################
    #### Bot for like and comment
    ############################################
    # Add likes to the post
    wait = WebDriverWait(driver, 10)
    like_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[4]/div/button[1]')))
    like_button.click()
    time.sleep(5)

    # Add comment to the post
    # Select a random comment from the list
    comment_text = random.choice(comments)
    # Create an instance of ActionChains
    # Move to the element to make it visible
    comment_click = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div/div/div[1]/div')
    actions = ActionChains(driver)
    actions.move_to_element(comment_click)
    actions.perform()
    comment_click.click()
    comment_input = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div/div/div[1]/div/div[1]/div/div/div[2]/div/div/div/div/span')))
    comment_input.send_keys(comment_text)
    time.sleep(2)
    comment_input.send_keys(Keys.ENTER)
    time.sleep(2)
        
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
