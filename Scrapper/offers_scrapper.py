#!/usr/bin/env python
# coding: utf-8

# In[43]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException , ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time


# In[7]:


url_1 = 'https://www.glassdoor.com/Job/morocco-jobs-SRCH_IL.0,7_IN162.htm'
url_2 = 'https://ma.indeed.com/?from=jobsearch-empty-whatwhere'
url_3 = 'https://www.linkedin.com/jobs/search?keywords=&location=Morocco&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'


# In[19]:


from selenium.webdriver.chrome.service import Service
service = Service('M:/chromedriver-win64/chromedriver-win64/chromedriver.exe')


# In[93]:


#opt = webdriver.ChromeOptions()
#opt.add_argument('headless')
driver = webdriver.Chrome(service= service)


# In[122]:


# scrapping url_1 : glassdor
driver.get(url_1)


# In[123]:


# Parameters of the search
post = 'Data Scientist'
location = 'Casablanca'


# In[124]:


search_bar_job = driver.find_element(By.ID,'searchBar-jobTitle')
search_bar_location = driver.find_element(By.ID,'searchBar-location')

search_bar_job.send_keys(post)

search_bar_job.send_keys(Keys.ENTER)


# In[125]:


import csv

with open('Jobs.csv','w') as f :
    header = ['Job','Employer' ,'Employer Rating','Location','Description']
    writer = csv.writer(f , delimiter =';')
    writer.writerow(header)


# In[126]:


# Find the jobs
jobs = driver.find_elements(By.CLASS_NAME , 'JobCard_jobCardContainer__l0svv')
i=0

# loop through the jobs
for job in jobs :
    job.click()
    time.sleep(2)
    job_details = driver.find_element(By.CLASS_NAME , 'JobDetails_jobDetailsContainer__sS1W1')
    title = job_details.find_element(By.CLASS_NAME,'JobDetails_jobTitle__Rw_gn').text
    
    if title.lower().find('data') != -1 :
        
        employer = job_details.find_element(By.CLASS_NAME , 'EmployerProfile_employerName__Xemli').text
        
        # Some employers don't have rating
        try : 
            employer_rating = job_details.find_element(By.CLASS_NAME , 'EmployerProfile_ratingContainer__N4hxE').text
        except NoSuchElementException:
            pass
        
        location = job_details.find_element(By.CLASS_NAME , 'JobDetails_location__MbnUM').text
        
        try :
            more_button = job_details.find_element(By.CLASS_NAME , 'JobDetails_showMore__j5Z_h')
            
            try :
                more_button.click()
                
            except ElementClickInterceptedException :
                wait = WebDriverWait(driver, 20)
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'CloseButton'))).click()
                
                
        except NoSuchElementException :
            pass
        
        job_description = job_details.find_element(By.CLASS_NAME , 'JobDetails_jobDescription__6VeBn').text

        job_infos = [title,employer,float(employer_rating),location,job_description]
        
        with open('Jobs.csv','a') as f :
            writer = csv.writer(f , delimiter =';')
            writer.writerow(job_infos)
            i+= 1
        
        
        
            


# In[57]:


# Scrapping url_2 : Indeed 
post = 'Data Scientist'
town = 'Casablanca'
driver.get(url_2)


# In[58]:


search_bar_text = driver.find_element(By.ID , 'text-input-what')
search_bar_text.send_keys(post)

search_bar_town = driver.find_element(By.ID , 'text-input-where')
search_bar_town.send_keys(town)

search_button = driver.find_element(By.CLASS_NAME,'yosegi-InlineWhatWhere-primaryButton')
search_button.click()


# In[59]:


while True :
    jobs = driver.find_elements(By.CLASS_NAME , 'css-mk9n32')
    
    for job in jobs :
        try :
            job.click()
            time.sleep(3)
            
        except ElementClickInterceptedException :
            wait = WebDriverWait(driver, 20)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="fermer"]'))).click()
            
        
        job_details = driver.find_element(By.CLASS_NAME , 'jobsearch-JobComponent')
        title = job_details.find_element(By.CLASS_NAME , 'jobsearch-JobInfoHeader-title').text

        if title.lower().find('data') != -1 :
            try :
                employer = job_details.find_element(By.CLASS_NAME , 'css-1saizt3').text
            except NoSuchElementException :
                employer = job_details.find_element(By.CLASS_NAME,'css-1cxc9zk').text

            location = job_details.find_element(By.CLASS_NAME , 'css-1ikmi61').text
            description = job_details.find_element(By.ID , 'jobDescriptionText').text
            employer_rating = None

            job_infos = [title,employer,employer_rating,location,job_description]

            with open('Jobs.csv','a') as f :
                writer = csv.writer(f , delimiter =';')
                writer.writerow(job_infos)
                i+= 1
                print(i)
    try :           
        next_page_button = driver.find_element(By.XPATH , '//a[@aria-label="Next Page"]')
        next_page_button.click()
        
    except NoSuchElementException :
        break


# In[105]:


#Scrapping url_3

# scrapping url_3 : LinKedIn
driver.get(url_3)


# In[106]:


search_bar = driver.find_element(By.ID , 'job-search-bar-keywords')
search_bar.send_keys(post)
search_bar.send_keys(Keys.ENTER)


# In[107]:


## Scrolling til the end to show all the offers
SCROLL_PAUSE_TIME = 20

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


# In[109]:


jobs = driver.find_elements(By.CLASS_NAME , 'job-search-card')

for job in jobs :
        job.click()
        time.sleep(5)
        
        try:
            title = driver.find_element(By.CLASS_NAME , 'top-card-layout__title').text
        except NoSuchElementException :
            driver.back()
            time.sleep(3)
        
        try :
            employer = driver.find_element(By.CLASS_NAME , 'topcard__org-name-link').text
        except NoSuchElementException :
            employer = driver.find_elements(By.TAG_NAME , 'span')[0].text
            
        location = driver.find_element(By.CLASS_NAME ,'topcard__flavor--bullet').text

        try:
            more_button =  driver.find_element(By.CLASS_NAME , 'show-more-less-button')
            more_button.click()

        except NoSuchElementException :
            pass

        description = driver.find_element(By.CLASS_NAME , 'show-more-less-html__markup ').text
        employer_rating = None
        driver.back()
        
        job_infos = [title,employer,employer_rating,location,job_description]
        with open('Jobs.csv','a') as f :
                writer = csv.writer(f , delimiter =';')
                writer.writerow(job_infos)
                i+= 1
                print(i)

        


# In[ ]:




