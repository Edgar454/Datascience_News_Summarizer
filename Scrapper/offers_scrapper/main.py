from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from functions import Glassdor_scrapper , LinKedIn_scrapper , Indeed_scrapper
import time

service = Service('M:/chromedriver-win64/chromedriver-win64/chromedriver.exe')
#opt = webdriver.ChromeOptions()
#opt.add_argument('headless')
driver = webdriver.Chrome(service= service)

print("="*10,'Beginning the research',"="*10)

class Params :
    job = 'Data Scientist'
    location = 'Casablanca'

print("="*10,'Scrapping Glassdor',"="*10)

# scraper = Glassdor_scrapper(driver)
# scraper.get_offers(Params.job)
# number_offers_Glassdor = scraper.scrape_offers()

# print(f'Offers_scrapped : {number_offers_Glassdor}')


print("="*10,'Scrapping Indeed',"="*10)

# scraper = Indeed_scrapper(driver)
# scraper.get_offers(Params.job,Params.location)
# number_offers_Indeed = scraper.scrape_offers()

# print(f'Offers_scrapped : {number_offers_Indeed}')


print("="*10,'Scrapping LinkedIn',"="*10)

scraper = LinKedIn_scrapper(driver)
scraper.get_offers(Params.job)
number_offers_linkedIn = scraper.scrape_offers()

print(f'Offers_scrapped : {number_offers_linkedIn}')

total_number_scrapped = number_offers_linkedIn + number_offers_Indeed + number_offers_Glassdor

print(f'Number total of offers scrapped {total_number_scrapped}')


#if __name__ = '__main__' :