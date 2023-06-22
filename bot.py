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

proxy_file_path = 'proxy.txt'

# Read Proxies texts from the text file
proxies = []
with open(proxy_file_path, 'r') as file:
    for line in file:
        proxies.append(line.strip())
# Instantiate the Chrome WebDriver
# driver = webdriver.Chrome()
# Add any desired options to the options object, if needed
# options = uc.ChromeOptions()
# driver = uc.Chrome(options=options)

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# Add the --mute-audio flag
options.add_argument("--mute-audio")

# options.add_argument(f'--proxy-server={random.choice(proxies)}')

# options.add_argument("--headless")

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
start_row = 85  # Replace with the starting row index
end_row = 91  # Replace with the ending row index

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

# Read comment texts from the text file
comments = []
with open(comments_file, "r") as file:
    for line in file:
        comment = line.strip()
        comments.append(comment)

# Iterate over each account
for account in accounts:
    
    try:
        # Set the proxy IP address and port
        proxy = random.choice(proxies).split(":")
        proxy_ip = proxy[0] #'199.102.105.242'
        proxy_port = proxy[1] #'4145'

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
        print(f'Account {account["username"]} is logging in...')

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
        print(f'Account {account["username"]} Success...')
    except ValueError:
        print(f'Account {account["username"]} Failed...')
        # Code to handle ValueError exception
        print("ValueError occurred!")
    except TypeError:
        print(f'Account {account["username"]} Failed...')
        # Code to handle TypeError exception
        print("TypeError occurred!")
    except Exception as e:
        print(f'Account {account["username"]} Failed...')
        # Code to handle any other exceptions


# Close the browser
driver.quit()
