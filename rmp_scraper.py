import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
from sqlalchemy import create_engine


#HELPER FUNCTIONS

def parse_firstname(name):
    try:
        space = name.index(' ')
    except:
        space = len(name)
        print("No space: "+name)
    return name[ :space]

def parse_lastname(name):
    try:
        space = name.index(' ')
    except:
        space = -1
        print("No space: "+name)
    return name[space+1 : ]


def expand_results(driver):
    errors=0
    wait = WebDriverWait(driver, 10)
    header = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[4]/div[1]/div[1]/div/h1')))
    num_results = int(parse_firstname(header.text))
    if(num_results<9):
        return
    button = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[4]/div[1]/div[4]/button')
    for i in range(int((num_results-1)/8)):
        try: 
            button.click()
            errors=0
        except:
            i-=1
    
        print(i+1)
        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[4]/div[1]/div[4]/button')))
            #time.sleep(5)
            button.click()
        except:
            return
        

def get_data(driver, rmp_data):
    teachers = driver.find_elements_by_class_name('TeacherCard__StyledTeacherCard-syjs0d-0')
    print(len(teachers))
    for i in range(len(teachers)):
        rating = teachers[i].find_element_by_class_name('CardNumRating__CardNumRatingNumber-sc-17t4b9u-2').text
        name = teachers[i].find_element_by_class_name('CardName__StyledCardName-sc-1gyrgim-0').text
        numRatings = teachers[i].find_element_by_class_name('CardNumRating__CardNumRatingCount-sc-17t4b9u-3').text
        rmp_data = rmp_data.append({'First Name' : parse_firstname(name), 'Last Name' : parse_lastname(name), 'Rating' : rating, 'No. of Ratings': numRatings}, ignore_index = True)

    return rmp_data
    
        

#SCRIPT:


driver = webdriver.Chrome('/Users/sam/ChromeExtensionScrapingHelloWorld/env/chromedriver')
driver.get('https://www.ratemyprofessors.com/search/teachers?query=*&sid=675')
wait = WebDriverWait(driver, 10)

time.sleep(2) # Let the user actually see something!

rmp_data = pd.DataFrame(columns = ['First Name', 'Last Name', 'Rating', 'No. of Ratings'])
dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[4]/div[1]/div[2]/div/div[2]/div')))
dropdown.click()

for i in range(94): #94 categories on RMP
    id= 'react-select-'+str(i+3)+'-option-'+str(i+1)
    menu_option = wait.until(EC.element_to_be_clickable((By.ID, id)))
    #time.sleep(1)
    menu_option.click()
    expand_results(driver)
    rmp_data=get_data(driver, rmp_data)
    driver.execute_script("window.scrollTo(0,0);") #SUPER IMPORTANT
    try:
        driver.find_element(By.CLASS_NAME, 'Header__StyledHeader-sc-1oduwjk-1').click()
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[4]/div[1]/div[2]/div/div[2]/div/div[1]')))
        dropdown.click()
        
    except:
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[4]/div[1]/div[2]/div/div[2]/div/div[1]')))
        dropdown.click()


time.sleep(5)

driver.quit()

rmp_data.drop_duplicates(subset=['First Name', 'Last Name', 'Rating'], keep='first', inplace=True)

engine = create_engine('sqlite:///rmp_data.db', echo=True)
sqlite_connection = engine.connect()

sqlite_table = "RateMyProfRatings"
rmp_data.to_sql(sqlite_table, sqlite_connection, if_exists='replace')

sqlite_connection.close()

    