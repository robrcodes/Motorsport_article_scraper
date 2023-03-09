from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime

# get today's date to add to bottome of article text file
today_date = datetime.today()

# required: bs4, requests, lxml

# initial website address to scrape
website = 'https://www.speedcafe.com/'
result = requests.get(website)
content = result.content

# parse html into soup object
soup = bs(content, 'lxml')

# focus scraping onto featured article div of main page
main_box = soup.find('div', class_='post-block-first')

# identify the featured article title
mb_title = main_box.find('h4', class_='entryTitle')


# identify the featured article page link
page_link = mb_title.find('a', class_='animate').get('href')

# scrape the page content of the featured article
feature_result = requests.get(page_link)
feature_content = feature_result.content
feature_soup = bs(feature_content, 'lxml')

# identify and focus scraping to article entry on the page
main_content = feature_soup.find('div', class_='entryContent')

# Use CSS selector to specify only the required content, the article text, goes into the list
feature_article = main_content.select('div.entryContent > p')

# get the article date meta 
published_date = feature_soup.find('p', class_='date meta')

# current format date text is displayed on page
format = '%A %d %B %Y %I:%M%p'

# clean text date to simplify conversion to date object
mydate = published_date.get_text().replace('th', '').replace(',','').replace('- ','')

# create date object from text date
dateobj = datetime.strptime(mydate, format)

# write the list of the article content into a text file using a loop to add each list element
with open(f'{dateobj.date()}-{dateobj.time()}-{mb_title.get_text()[0:20]}.txt', 'w') as file:
    file.write(mb_title.get_text().upper())
    for para in feature_article:
        # write each line into file
        file.write("%s\n\n" % para.get_text())

    # add today's date at bottom of article text file
    file.write('Extracted: ')
    file.write("%s\n\n" % today_date)
    
    # close the file once complete
    file.close()