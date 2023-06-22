const webdriver = require('selenium-webdriver');
const { Builder, By, Key, until } = webdriver;
const chrome = require('selenium-webdriver/chrome');
const CaptchaSolver = require('tiktok-captcha-solver');
const puppeteer = require('puppeteer');

const logged_in_accounts = new Set(); // Keep track of logged-in accounts

const ua = require('random-useragent');
const user_agent = ua.getRandom();

async function loginTikTok(accounts, proxies, targetUrl, comments) {
  // Iterate over each account
  for (const account of accounts) {
    const browser = await puppeteer.launch({
        headless: false, // Set to false for visible browser windows
        args: [
          '--start-maximized',
          '--mute-audio',
          '--no-sandbox',
          '--disable-dev-shm-usage',
          `--user-agent=${user_agent}`,
        ],
      });

    const chromePath = 'chromedriver.exe';
    
    // const service = new chrome.ServiceBuilder().build();
    // const service = new chrome.ServiceBuilder(chromePath).build();
    // console.log(chrome);
    // chrome.setDefaultService(service);

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 }); // Set viewport size

    //   the captcha solver should be initialized before visiting the page
    const captchaSolver = new CaptchaSolver(page)

    captchaSolver.solve({
        numAttempts: 5, // max number of attempts to solve the captcha
        startPosition: 25, // start position of the slider handle
        positionIncrement: 5, // number of pixels to advance the slider on each iteration
      })

    const username = account.username;
    const password = account.password;
    const proxy = proxies[Math.floor(Math.random() * proxies.length)];
    const comment = comments[Math.floor(Math.random() * comments.length)];

    if (logged_in_accounts.has(username)) {
      console.log(`Account ${username} is already logged in. Skipping...`);
      await browser.close();
      continue;
    }

    // // Set up Chrome options
    // const chromeOptions = {
    //   'args': [
    //     '--mute-audio',
    //     `--proxy-server=${proxy}`,
    //     '--no-sandbox',
    //     '--disable-dev-shm-usage',
    //     `--user-agent=${user_agent}`,
    //   ]
    // };

    // // Create a new WebDriver instance
    // const driver = await new Builder()
    //   .forBrowser('chrome')
    //   .setChromeOptions(chromeOptions)
    //   .build();

    try {
      console.log(`Account ${username} is logging in...`);

      await page.goto('https://www.tiktok.com/login/phone-or-email/email');

      await page.waitForSelector('input[name="username"]', { timeout: 10000 });
      await page.type('input[name="username"]', username);

      await page.waitForSelector('input[type="password"]', { timeout: 10000 });
      await page.type('input[type="password"]', password);

      await page.waitForTimeout(5000);

      // Press Enter to submit the login form
      await page.keyboard.press('Enter');

      // solve the captcha
      // await page.waitForXPath('/html/body/div[9]/div');
      await captchaSolver.solve()

      await page.waitForNavigation({ url: 'https://www.tiktok.com' });

      // Example: Check if login was successful
      if (page.url().includes('login')) {
        throw new Error('Login failed');
      } else {
        // Navigate to the target URL
        await page.goto(targetUrl);
      }

      // Add the account to the set of logged-in accounts
      logged_in_accounts.add(username);
       // Bot for like and comment
       await page.waitForXPath('/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[4]/div/button[1]');
       const [likeButton] = await page.$x('/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[4]/div/button[1]');
       const [tagElement] = await page.$x('/html/body/div[1]/div[3]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div[4]/div/button[1]/span/div/div/svg/g/g[2]/g/g[4]');
 
      // Get the value of the 'style' attribute
      const styleValue = await tagElement.evaluate((element) => element.getAttribute('style'));

      // Perform a conditional action based on the style value
      if (!styleValue.includes('display: none;')) {
        await likeButton.click();
        await page.waitForTimeout(5000);

        // Add comment to the post
        const [commentClick] = await page.$x('/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div/div/div[1]/div');
        // const actions = driver.actions({ bridge: true });
        // await actions.move({ origin: commentClick }).perform();
        // await commentClick.click();

        // const commentInput = await driver.wait(until.elementLocated(By.xpath('/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div[1]/div/div/div[1]/div/div[1]/div/div/div[2]/div/div/div/div/span')));
        // await commentInput.sendKeys(comment);
        // await driver.sleep(2000);
        // await commentInput.sendKeys(Key.ENTER);
        // await driver.sleep(2000);
      }

      // Logout and clear cookies for the next account
      // Delete all cookies
      const cookies = await page.cookies();
      await page.deleteCookie(...cookies);
    } catch (error) {
      console.log(`Error during login: ${error.message}`);
    } finally {
      await browser.close();
    }
  }
}

async function main() {
  const workers = 5; // multi-instance

  // Specify the file path of the Excel file
  const excelFile = 'AKUN GMAIL.xlsx';

  // Path to the external text file containing comment texts
  const commentsFile = 'comments.txt';

  // Path to the text file containing proxy addresses
  const proxyFilePath = 'proxy.txt';

  // URL to navigate to after logging in
  const targetUrl = 'https://www.tiktok.com/@nikxphreaker/video/6993669592551836930';

  // Read account credentials from the Excel file
  const accounts = [];
  const sheetName = 'MARSHA'; // Specify the sheet name if it's not the default sheet

  // Specify the columns and rows you want to extract
  const columns = ['Gmail', 'Password.2']; // Replace with your desired column names
  const startRow = 50; // Replace with the starting row index
  const endRow = 54; // Replace with the ending row index

  // Read the Excel file
  const XLSX = require('xlsx');
  const workbook = XLSX.readFile(excelFile);
  const worksheet = workbook.Sheets[sheetName];

  const data = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

  // Extract the desired data range
  const selectedData = data.slice(startRow - 1, endRow);

  // Find the column indices based on column names
  // const column1Index = selectedData.indexOf(columns[0]);
  // const column2Index = selectedData.indexOf(columns[1]);

  // Extract data from the specified columns
  // const dataArray = selectedData.map(row => {
  //   if (row[1] != undefined || row[10] != undefined) {
  //     continue; // Skip rows with invalid data
  //   } else {
  //     [row[1], row[10]]
  //   }
    
  // });

  // console.log(selectedData);
  // console.log(dataArray);

  // // Convert the selected data into a list of objects
  for (const row of selectedData) {
    const username = row[1];
    const password = row[10];

    if (username == undefined || password == undefined) {
      continue; // Skip rows with invalid data
    }

    const account = { 'username' : username, 'password' : password };
    console.log(account);
    accounts.push(account);
  }

  // Read proxy addresses from the text file
  const fs = require('fs');
  const proxies = fs.readFileSync(proxyFilePath, 'utf-8').split('\n').map(line => line.trim()).filter(line => line !== '');

  // Read comment texts from the text file
  const comments = fs.readFileSync(commentsFile, 'utf-8').split('\n').map(line => line.trim()).filter(line => line !== '');

  const numPieces = 5; // Number of pieces to split the array into
  const arrayLength = accounts.length;
  const pieceSize = Math.floor(arrayLength / numPieces);
  const remainder = arrayLength % numPieces;

  const splitArrays = [];
  let start = 0;
  for (let i = 0; i < numPieces; i++) {
    const end = start + pieceSize + (i < remainder ? 1 : 0); // Adjust piece size for the remainder
    splitArrays.push(accounts.slice(start, end));
    start = end;
  }

  //Create an array of promises for each WebDriver instance
  const promises = splitArrays.map((accounts) => loginTikTok(accounts, proxies, targetUrl, comments));

  // Execute all promises concurrently
  await Promise.all(promises);

  console.log('All Selenium instances have completed.');
}

main().catch(console.error);
