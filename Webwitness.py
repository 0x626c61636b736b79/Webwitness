from selenium import webdriver
from stem import Signal
from stem.control import Controller
webdriver_path = "C:/Users/Hp/Desktop/chromedriver.exe"
tor_binary_path = "C:/Path/To/Tor/tor.exe"

# Function to change the Tor circuit
def change_tor_circuit():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()  # Authenticate with the Tor controller
        controller.signal(Signal.NEWNYM)  # Signal Tor to create a new circuit
tor_proxy = "socks5://127.0.0.1:9050"  # 
print("[+] Press 1. for single url [+]")
print("[+] Press 2. for multiple url [+]")
url = int(input("Please choose a number(1. single 2.text file): "))
if url==1:
    single_url_input = input("Please enter the url: ")
    options = webdriver.ChromeOptions()
    options.add_argument(f'--proxy-server={tor_proxy}')

    options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
    driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
    try:
    # Navigate to the URL
        driver.get(single_url_input)
        change_tor_circuit()
        # Capture a screenshot of the webpage
        driver.save_screenshot('screenshot.png')  # Save the screenshot to a file
        print(f'Screenshot saved as screenshot.png')
    except Exception as e:
            print(f'An error occurred: {e}')
    finally:
            # Close the browser
            driver.quit()
elif url == 2:
    url_list_file = input("Please enter the location where the list is saved: ")
    
    try:
        with open(url_list_file, 'r') as urls:
            urls_list = urls.readlines()
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
        driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
        
        for i, url in enumerate(urls_list):
            url = url.strip()  # Remove leading/trailing whitespaces
            
            try:
                # Navigate to the URL
                driver.get(url)
                
                # Capture a screenshot of the webpage
                screenshot_filename = f'screenshot_{i}.png'
                driver.save_screenshot(screenshot_filename)  # Save the screenshot to a file
                print(f'Screenshot saved as {screenshot_filename} for URL: {url}')
            except Exception as e:
                print(f'An error occurred for URL {url}: {e}')
    except Exception as e:
        print(f'An error occurred while processing the URL list: {e}')
    finally:
        # Close the browser
        driver.quit()
