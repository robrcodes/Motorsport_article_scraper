from bs4 import BeautifulSoup as bs
import requests

# required: bs4, requests, lxml

# initial website address to scrape
website = 'https://www.speedcafe.com/'
result = requests.get(website)
content = result.text

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
feature_content = feature_result.text
feature_soup = bs(feature_content, 'lxml')

# identify and focus scraping to article entry on the page
main_content = feature_soup.find('div', class_='entryContent')

# Use CSS selector to specify only the required content, the article text, goes into the list
feature_article = main_content.select('div.entryContent > p')

# write the list of the article content into a text file using a loop to add each list element
with open(f'SC-{mb_title.get_text()}.txt', 'w') as file:
    file.write(mb_title.get_text().upper())
    for para in feature_article:
        # write each line into file
        file.write("%s\n\n" % para.get_text())

    # close the file once complete
    file.close()