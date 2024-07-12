from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException , ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service

import time
import csv

service = Service('M:/chromedriver-win64/chromedriver-win64/chromedriver.exe')

#opt = webdriver.ChromeOptions()
#opt.add_argument('headless')
driver = webdriver.Chrome(service= service)

url_1 = 'https://www.glassdoor.com/Job/morocco-jobs-SRCH_IL.0,7_IN162.htm'
url_2 = 'https://ma.indeed.com/?from=jobsearch-empty-whatwhere'
url_3 = 'https://www.linkedin.com/jobs/search?keywords=&location=Morocco&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'



with open('Jobs.csv','w',encoding='utf-8') as f :
    header = ['Job','Employer' ,'Employer Rating','Location','Description']
    writer = csv.writer(f , delimiter =';')
    writer.writerow(header)



class Glassdor_scrapper :
    
    def __init__(self , driver = driver):
        self.driver = driver
    
    def get_offers(self ,query):

        self.driver.get(url_1)
        search_bar_job = self.driver.find_element(By.ID,'searchBar-jobTitle')
        search_bar_location = self.driver.find_element(By.ID,'searchBar-location')

        search_bar_job.send_keys(query)
        search_bar_job.send_keys(Keys.ENTER)
        
    def scrape_offers(self):
        jobs = self.driver.find_elements(By.CLASS_NAME , 'JobCard_jobCardContainer__l0svv')
        i = 0
        for job in jobs :
            try :
                job.click()
            except ElementClickInterceptedException :
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'CloseButton'))).click()
                
            time.sleep(2)
            self.scrape_one_offer()   
            i+= 1   
            
        return i
        
        
    def scrape_one_offer(self) :
        # all the details of the job
        job_details = self.driver.find_element(By.CLASS_NAME , 'JobDetails_jobDetailsContainer__sS1W1')
        
        # scrapping the name of the job
        title = job_details.find_element(By.CLASS_NAME,'JobDetails_jobTitle__Rw_gn').text

        if title.lower().find('data') != -1 :
            
            # scrapping the employer name =
            employer = job_details.find_element(By.CLASS_NAME , 'EmployerProfile_employerName__Xemli').text

            # Some employers don't have rating
            try : 
                employer_rating = job_details.find_element(By.CLASS_NAME , 'EmployerProfile_ratingContainer__N4hxE').text
            except NoSuchElementException:
                employer_rating = None
            
            # scrapping the location
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
            # scrapping the description
            job_description = job_details.find_element(By.CLASS_NAME , 'JobDetails_jobDescription__6VeBn').text
            job_infos = [title,employer,employer_rating,location,job_description]
            self.save_offers(job_infos)

    
    def save_offers(self,infos):
        
        with open('Jobs.csv','a',encoding='utf-8') as f :
            writer = csv.writer(f , delimiter =';')
            writer.writerow(infos)
            



class Indeed_scrapper :
    
    def __init__(self , driver = driver):
        self.driver = driver
    
    def get_offers(self ,query , location) :
        self.driver.get(url_2)
        search_bar_text = self.driver.find_element(By.ID , 'text-input-what')
        search_bar_text.send_keys(query)

        search_bar_town = self.driver.find_element(By.ID , 'text-input-where')
        search_bar_town.send_keys(location)

        search_button = self.driver.find_element(By.CLASS_NAME,'yosegi-InlineWhatWhere-primaryButton')
        search_button.click()
        
    def scrape_offers(self):
        
        while True :
            jobs = self.driver.find_elements(By.CLASS_NAME , 'css-mk9n32')
            i = 0
            for job in jobs :
                try :
                    job.click()
                    time.sleep(5)
                except ElementClickInterceptedException :
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="fermer"]'))).click()

                self.scrape_one_offer()   
                i+= 1
            try :           
                next_page_button = self.driver.find_element(By.XPATH , '//a[@aria-label="Next Page"]')
                next_page_button.click()

            except NoSuchElementException :
                break
            
        return i
        
        
    def scrape_one_offer(self) :
        
        # all the details of the job
        job_details = self.driver.find_element(By.CLASS_NAME , 'jobsearch-JobComponent')
        
        # scrape the name of the job
        title = job_details.find_element(By.CLASS_NAME , 'jobsearch-JobInfoHeader-title').text

        if title.lower().find('data') != -1 :
            # scrape the employer name
            try :
                employer = job_details.find_element(By.CLASS_NAME , 'css-1saizt3').text
            except NoSuchElementException :
                employer = job_details.find_element(By.CLASS_NAME,'css-1cxc9zk').text
                
            # scrape the location
            location = job_details.find_element(By.CLASS_NAME , 'css-1ikmi61').text
            
            # scrape the description
            job_description = job_details.find_element(By.ID , 'jobDescriptionText').text
            
            # scrape the employer_rating
            employer_rating = None

            job_infos = [title,employer,employer_rating,location,job_description]
            self.save_offers(job_infos)
            
            
    
    def save_offers(self, info):
        
        with open('Jobs.csv','a',encoding='utf-8') as f :
            writer = csv.writer(f , delimiter =';')
            writer.writerow(info)
            






class LinKedIn_scrapper :
    
    def __init__(self , driver = driver):
        self.driver = driver
    
    def get_offers(self ,query) :

        self.driver.get(url_3)
        time.sleep(10)
        search_bar = driver.find_element(By.ID , 'job-search-bar-keywords')
        search_bar.send_keys(query)
        search_bar.send_keys(Keys.ENTER)
        
    def scroll_the_page(self):
        
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
        
    def scrape_offers(self):
        self.scroll_the_page()
        jobs = driver.find_elements(By.CLASS_NAME , 'job-search-card')
        i = 0
        for job in jobs :
            job.click()
            time.sleep(5)
            results = self.scrape_one_offer()   
            self.save_offers(results)
            i+= 1
        return i
        
        
    def scrape_one_offer(self) :
        try:
            title = self.driver.find_element(By.CLASS_NAME , 'top-card-layout__title').text
        except NoSuchElementException :
            self.driver.back()
            time.sleep(3)
        
        try :
            employer = self.driver.find_element(By.CLASS_NAME , 'topcard__org-name-link').text
        except NoSuchElementException :
            employer = self.driver.find_elements(By.TAG_NAME , 'span')[0].text
            
        location = self.driver.find_element(By.CLASS_NAME ,'topcard__flavor--bullet').text

        try:
            more_button =  self.driver.find_element(By.CLASS_NAME , 'show-more-less-button')
            more_button.click()

        except NoSuchElementException :
            pass

        job_description = self.driver.find_element(By.CLASS_NAME , 'show-more-less-html__markup ').text
        employer_rating = None
        driver.back()
        
        job_infos = [title,employer,employer_rating,location,job_description]
            
        return job_infos
    
    def save_offers(self,infos):
        
        with open('Jobs.csv','a',encoding='latin-1') as f :
            writer = csv.writer(f , delimiter =';')
            writer.writerow(infos)
            
