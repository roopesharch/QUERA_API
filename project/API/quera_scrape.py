from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4
import re
import random
import logging
import logging.handlers
import pickle
import pyautogui
import csv


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%chromedriver path%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
driver_path="/Users/roopesharch/project/API/chromedriver"
time.sleep(random.randint(3,6))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%customize chrome options%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
chrome_option = webdriver.ChromeOptions()
chrome_option.add_argument("--disable-notifications")
# chrome_option.add_argument('--headless')
chrome_option.add_argument("--incognito")
chrome_option.add_argument("--start-maximized")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%initiate to open browser%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
connection_attempt=0
while True:
    connection=0
    connection_attempt=connection_attempt+1
    try:
        driver = webdriver.Chrome(executable_path= driver_path,chrome_options=chrome_option)
        driver.maximize_window()
        br=1
        connection=1
        print("\n Connection successfull")
    except Exception as e:
        print(e)
        driver_path=input()
        
    if connection==1 or connection_attempt > 5:
        break

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Create CSV file %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
with open("Account_Names.csv", "w") as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(["Account_Names","Status"])
        
        
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%quera url supplied to browser%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
print("\n Started the launch")
driver.get("https://www.quora.com/")
driver.implicitly_wait(10)
time.sleep(random.randint(3,10))
print("\n Launched")

exit() 

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%login with credentials %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def login():
    attempt=0
    user="qasun06@gmail.com"
    pas="P@SSw0rd!"

    timeout=50

    try:
        myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'email')))
        driver.find_element_by_id("email").send_keys(user)
        time.sleep(random.randint(3,6))
        print ("\n Emial issued")
        attempt=attempt+1
    except Exception as e:
        print ("\n Email--not--accessed",e)


    try:
        myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'password')))
        driver.find_element_by_id("password").send_keys(pas)
        time.sleep(random.randint(3,6))
        print ("\n Password issued")
        attempt=attempt+1
    except Exception as e:
        print ("\n Password--not--accessed",e)


    time.sleep(random.randint(3,6))
    try:
        myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'qu-color--white')))
        driver.find_element_by_class_name("qu-color--white").click()
        time.sleep(random.randint(1,3))
        print ("\n Credentials Submitted")
        attempt=attempt+1
    except Exception as e:
        print ("\n Credentials--not--Submitted",e)
    
    return attempt


#%%%%%%%%%%%%%%%%%%%%%%%%%% Auto quit code after 5 attemps for login %%%%%%%%%%%%%%%%%%%%%%%%%%
loging=0  
attempt=0
while loging != 3 :
    loging=login()  
    attempt=attempt+1
    if attempt == 5 :
        driver.close()
        print("\n login--failed--check--internet--connection")
        



def home_load():

    timeout = 50 # Logged in So now it checks for home screen loaded or not  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    try:
        myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'lhMPoC')))
        try:
            myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'small_close')))
            try:
                myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[text()="What is your question or link?"]')))
                return 3
            except Exception as e:
                print("\n home_load Error due  to : )))))= ",e)
        except Exception as e:
            print("\n home_load Error due to : )))))= ",e)
    except Exception as e:
        print("\n home_load Error due to : )))))= ",e)

    return 
def load_home():
    home_loads=0
    home_attempt=0
    while home_loads !=3 :
        home_loads=home_load()
        home_attempt=home_attempt+1
        if home_load ==3:
            print("\n Home loaded successfuly")
        if home_attempt == 3 :
            print("\ncould not load home page")
            driver.close()
    
    
def check_accounts_count():
    file = open("Account_Names.csv")
    reader = csv.reader(file)
    lines= len(list(reader))-1
    return lines

def main_function():
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Check for Quera home screenv %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    load_home()
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Scroll to the bottom of page %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    time.sleep(random.randint(3,6))
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(random.randint(2,5))
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height   

    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Get account names into list people %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    try:
        people=[]
        content = driver.page_source
        soup = bs4.BeautifulSoup(content)
        for i in soup.find_all(class_="qu-size--36"):    
            i=str(i)
            if re.search( "for", i ):
                result = re.search('for(.*)" class="', i)   
                st=  str(result.group(1))
                st=  st.lstrip(' ')
                st=  st.rstrip(' ')
                if st in people or len(people) > 3:
                    pass
                else:

                    people.append(st)  
            else:
                pass
        print("\n All the account names in the page appended to list people and count =", len(people))   
    except Exception as e:
                print("\n BeautifulSoup Error due to : )))))= ",e)
            
            
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Iterate among the account names and DOWNLOAD HTML_DUMP %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    for name in reversed(people):
        
        
        #%%%%%%%%%%%%%%%%%%%%% check if the name is already in csv %%%%%%%%%%%%%%%%%%%%%
        data = pd.read_csv("Account_Names.csv")
        csv_list = data['Account_Names'].tolist()
        if name in csv_list:
            continue
        if len(csv_list) == 4:
            return check_accounts_count()
        
        timeout=50
        load_home()

        try:
            Account_name_path="//div/a/span[text()='"+name+"']"
            Account_name_check='//span[text()="'+name+'"]'
            myElem =WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,Account_name_check)))
            element=driver.find_element_by_xpath(Account_name_path)
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            time.sleep(random.randint(3,6))
            element.click()
            time.sleep(random.randint(2,4))
            driver.switch_to.window(driver.window_handles[1])
            print("\n Account",name,"scrape initiated | Account NO : ",check_accounts_count())
        except Exception as e:
            print("\n Click account  Error due to : )))))= ",e)
            main_function()
            return check_accounts_count()



        account_page_check=0
        def account_page_check():
            timeout=30
            attempt=0
            try:
                myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Credentials & Highlights"]')))
#                 print ("\n Credentials & Highlights detected")
                attempt=attempt+1
            except Exception as e:
                print("\n Credentials--&--Highlights--not--detected )))))= ",e)

            try:
                myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'qu-color--red')))
#                 print ("\n Profile detected")
                attempt=attempt+1
            except Exception as e:
                print ("\n Profile--not--detected )))))= ",e)
            try:
                myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'cDraHQ')))
#                 print ("\n More description detected")
                attempt=attempt+1
            except Exception as e:
                print ("\n More--description--not--detected )))))= ",e)
            return attempt

        check_count=0
        while account_page_check != 3 :
            print("\n Checking account page loading")
            account_page_check=account_page_check()
            check_count=check_count+1
            if check_count == 5:
                print("\n could not load the account new page")
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(2)
                driver.close();
                driver.switch_to.window(driver.window_handles[0])
                main_function()
                return check_accounts_count()
            
        print("\n The account new page is successfully loaded")

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Scroll to the bottom of page %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        try:
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Wait to load page
                time.sleep(random.randint(2,4))
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height  
        except Exception as e:
                print ("\n scroll not loading )))))= ",e)
                main_function()
                return check_accounts_count()

        time.sleep(random.randint(2,3))



        




        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Click all the more options %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
        more_count=0
       
        more = driver.find_elements_by_class_name('cDraHQ')
        for x in range(0,len(more)):
            if more[x].is_displayed():
                try:
                    timeout=20
                    actions = ActionChains(driver)
                    actions.move_to_element(more[x]).perform()
                    time.sleep(random.randint(1,2))
                    timeout=10
                    myElem = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'cDraHQ')))
                    more_count=more_count+1
                    more[x].click() 
                    time.sleep(random.randint(1,3))
                except Exception as e:
                    print ("\n Click all more options error )))))= ",e)
      
        print("\n More description accessed count = ",more_count)

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Save HTLM DUMP to destination path %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        html_saved=0
        try:
            content = driver.page_source
            html_path="/Users/roopesharch/project/API/HTML_DUMP/" + name + ".html"
            with open(html_path, 'w') as f:
                f.write(content)
            print("\n Saved html for ",name)  
            html_saved=1
        except Exception as e:
                    print ("\n Saving html error )))))= ",e)
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Append account name to csv %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if html_saved == 1:
            try:
                with open("Account_Names.csv", "a") as csvfile:
                    writer=csv.writer(csvfile)
                    writer.writerow([name,"Dumped HTML"])
            except Exception as e:
                        print ("\n Appending CSV error )))))= ",e)
    
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Get back to home screen %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        try:
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2)
            driver.close();
            driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
                        print ("\n Get back to home screen )))))= ",e)
    
    return check_accounts_count()
          
main_functions = 0
while main_functions < 4 :
    print("Initiating main function")
    main_functions=main_function() 
    
try:   
    driver.close()
    driver.close()
except:
    pass

Print("\n Fully completed")

