import concurrent.futures
from selenium import webdriver
from selenium_stealth import stealth
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
import random
import pandas as pd
import time

logged_in_accounts = set()  # Keep track of logged-in accounts

def login_tiktok(accounts, proxies, target_url, comments):

    # Iterate over each account
    for account in accounts:
        username = account["username"]
        password = account["password"]
        proxy = random.choice(proxies)
        comment = random.choice(comments)

        if username in logged_in_accounts:
            print(f"Account {username} is already logged in. Skipping...")
            return

        # Generate a random user agent
        user_agent = UserAgent().random

        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument(f'--user-agent={user_agent}')
        # options.add_argument(f'--proxy-server={proxy}')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        webdriver_path = 'chromedriver.exe'

        # stealth(driver,
        #         languages=["en-US", "en"],
        #         user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
        #         vendor="Google Inc.",
        #         platform="Win32",
        #         webgl_vendor="Intel Inc.",
        #         renderer="Intel Iris OpenGL Engine",
        #         fix_hairline=True,
        #         )

        print(f"Account {username} is Login.")
        # driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
        driver = webdriver.Chrome(options=options)

        try:
            print(f"Account {username} is Login.")

            driver.get("https://www.tiktok.com/login/phone-or-email/email")

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))

            email_field = driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
            email_field.send_keys(username)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
            password_field = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
            password_field.send_keys(password)
            time.sleep(5)

            # Press Enter to submit the login form
            password_field.send_keys(Keys.ENTER)

            WebDriverWait(driver, 10).until(EC.url_to_be('https://www.tiktok.com'))

            # Example: Check if login was successful
            if "login" in driver.current_url:
                raise Exception("Login failed")
            else:
                # Navigate to the target URL
                driver.get(target_url)

            # Add the account to the set of logged-in accounts
            logged_in_accounts.add(username)

            ############################################
            #### Bot for like and comment
            ############################################
            # Add likes to the post
            wait = WebDriverWait(driver, 10)
            like_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[4]/div/button[1]')))
            like_button.click()
            time.sleep(5)

            # Add comment to the post
            # Create an instance of ActionChains
            # Move to the element to make it visible
            comment_click = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div/div/div[1]/div')
            actions = ActionChains(driver)
            actions.move_to_element(comment_click)
            actions.perform()
            comment_click.click()
            comment_input = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div/div/div[1]/div/div[1]/div/div/div[2]/div/div/div/div/span')))
            comment_input.send_keys(comment)
            time.sleep(2)
            comment_input.send_keys(Keys.ENTER)
            time.sleep(2)

            # Logout and clear cookies for the next account
            driver.delete_all_cookies()

        except NoSuchElementException as e:
            print(f"Element not found: {str(e)}")
        except Exception as e:
            print(f"Error during login: {str(e)}")

        finally:
            driver.quit()

def main():

    # Specify the file path of the Excel file
    excel_file = 'AKUN GMAIL.xlsx'

    # Path to the external text file containing comment texts
    comments_file = "comments.txt"

    proxy_file_path = 'proxy.txt'

    # URL to navigate to after logging in
    target_url = "https://www.tiktok.com/@nikxphreaker/video/6993669592551836930"

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

    # Read Proxies texts from the text file
    proxies = []
    with open(proxy_file_path, 'r') as file:
        for line in file:
            proxies.append(line.strip())

    # Read comment texts from the text file
    comments = []
    with open(comments_file, "r") as file:
        for line in file:
            comment = line.strip()
            comments.append(comment)

    num_pieces = 5  # Number of pieces to split the array into
    array_length = len(accounts)
    piece_size, remainder = divmod(array_length, num_pieces)

    split_arrays = []

    start = 0
    for i in range(num_pieces):
        end = start + piece_size + (i < remainder)  # Adjust piece size for the remainder
        split_arrays.append(accounts[start:end])
        start = end

    # for arr in split_arrays:
    #     print(arr)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for account in split_arrays:
            futures.append(
                executor.submit(
                    login_tiktok,
                    account,
                    proxies,
                    target_url,
                    comments,
                )
            )

        concurrent.futures.wait(futures)

if __name__ == '__main__':
    main()
