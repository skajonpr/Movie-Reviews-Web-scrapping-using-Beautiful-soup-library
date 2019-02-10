"""
Author: Sukit Kajonpradapkul

Decription: The program is to prompt the user for a link to review page, and the program acquires all the review and creates wordcloud.

"""
import urllib2
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt


# Get enteted link and the number of review pages
print "Please Enter a link to your moview reviews (it takes for a while to run depended on your internet speed...pls wait)"
print "For ex. https://www.rottentomatoes.com/m/instant_family/reviews/"
review_link = raw_input('Link = ')
base_url = review_link
open_base_url = urllib2.urlopen(base_url)
base_page_soup = BeautifulSoup(open_base_url, "lxml")

try:
    num_pages = int(base_page_soup.find_all(class_ ="pageInfo")[0].text.encode('utf-8').split()[3])
except:
    num_pages = 1

reviews_and_scores = []
nominal_scores = {'A+':1, 'A':0.96, 'A-':0.92, 'B+':0.89, 
            'B':0.86, 'B-':0.82,'C+':0.79,'C':0.76,'C-':0.72,'D+':0.69,'D':0.66,'D-':0.62, 'F':0.5}

                        
for page in range(num_pages):
    
    url_of_pages = '{}?page={}&sort='.format(review_link ,str(page+1))
    open_page = urllib2.urlopen(url_of_pages)
    soup = BeautifulSoup(open_page, "lxml")

    for i in range(len(soup.find_all(class_ = 'the_review'))):
        get_review_and_score=[]
        
        if "Original Score" in soup.find_all(class_ = 'small subtle')[i].text.encode('utf-8'):
            if soup.find_all(class_ = 'small subtle')[i].text.encode('utf-8').split()[5] in nominal_scores:
                
                get_review_and_score.append(soup.find_all(class_ = 'the_review')[i].text.replace('\n', ' ').strip().encode('utf-8'))
                
                get_numeric = nominal_scores[soup.find_all(class_ = 'small subtle')[i].text.encode('utf-8').split()[5]]
                get_review_and_score.append(get_numeric)
                
            else:
                get_review_and_score.append(soup.find_all(class_ = 'the_review')[i].text.replace('\n', ' ').strip().encode('utf-8'))
                
                if '/' in soup.find_all(class_ = 'small subtle')[i].text.encode('utf-8').split()[5]:
                    get_scorevalue = soup.find_all(class_ = 'small subtle')[i].text.encode('utf-8').split()[5]
                    get_review_and_score.append(float(get_scorevalue.replace('/',' ').split()[0])/float(get_scorevalue.replace('/',' ').split()[1]))
                else:
                    get_scorevalue = soup.find_all(class_ = 'small subtle')[i].text.encode('utf-8').split()[5]
                    get_review_and_score.append(get_scorevalue)     
        else:
            continue
        reviews_and_scores.append(get_review_and_score)


print 'Top 10 Rating and Review:'
for i in sorted(reviews_and_scores, key=lambda x : x[1])[-10:]:
   print i

print 
print 'Least 10 Rating and Review:'
for i in sorted(reviews_and_scores, key=lambda x : x[1])[0:11]:
   print i
   
# Create stopwords list and string of all review.
stpwords = set(stopwords.words('english'))
review_only = ' '.join([i[0] for i in reviews_and_scores])

#Function to create wordcloud ("string" variable has to be string)
def create_wordcloud(string):
    plt.figure('Review')
    wc = WordCloud(background_color="white", max_words=2000, stopwords=stpwords)              
    wc.generate(string)
    plt.imshow(wc)
    plt.axis('OFF')
    plt.title('Movie Review Wordcloud', color = 'g')
    plt.show()


# filter words of string and return filtered string
def stopword_filter(string):
    tokenize = string.split()    
    String_filter = [word for word in tokenize if word.isalpha()]        
    Filtered = [word for word in String_filter if word not in stpwords]
    return ' '.join(Filtered)


# Call function of wordcloud
try:
    create_wordcloud(stopword_filter(review_only))
except:
    print "The link entered is invalid"


            
        

            
                    
                
 

