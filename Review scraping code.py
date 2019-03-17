"""
Author: Sukit Kajonpradapkul

Decription: The program is to prompt the user for a link to review page, and the program acquires all the review and creates wordcloud.

"""
from selenium import webdriver
import time



def getFullData(movie_id):
        
    executable_path = 'geckodriver'
    driver = webdriver.Firefox(executable_path=executable_path)
    driver.implicitly_wait(10)
    driver.get('https://www.rottentomatoes.com/m/{}/reviews/'.format(movie_id))
    
    num_page = driver.find_element_by_xpath("//span[@class = 'pageInfo']").text.split()[-1]
    
    list_of_review = []
    for page in range(int(num_page)):
        
        try:                  
            date = driver.find_elements_by_xpath("//div[@class = 'review_date subtle small']")
            review = driver.find_elements_by_xpath("//div[@class = 'the_review']")
            rating = driver.find_elements_by_xpath("//div[@class = 'small subtle']")
            
            for item in range(len(review)):
                if len(rating[item].text.split(':')) > 1:
                    score = rating[item].text.split(':')[-1].strip()
                else:
                    score = ""
                list_of_review.append((date[item].text, \
                review[item].text, \
                score))
                        
        except:
            print ("error on page {}".format(page+1))
            
        page_link = driver.find_elements_by_xpath("//a[@class = 'btn btn-xs btn-primary-rt']")[-1]
        page_link.click()
        time.sleep(1)
        
    return list_of_review 
    



            
        

            
                    
                
 

