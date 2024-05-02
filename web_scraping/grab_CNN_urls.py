from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import csv


def get_next_url(soup):
    p_tag = soup.find_all('p', class_='cnnBodyText')[1]
    a_tag = p_tag.find('a') if p_tag else None

    # Get the 'href' attribute if the <a> tag is found
    href_value = a_tag['href'] if a_tag else 'No link found'

    return "https://transcripts.cnn.com/show/cnnt" + href_value

url = 'https://transcripts.cnn.com/show/cnnt'
response = requests.get(url)

# Initialize a list to store the links
links = []

while(response.status_code == 200):
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all elements with the class 'cnnSectBulletItems'
    elements_with_class = soup.find_all('div', class_='cnnSectBulletItems')
    # next_button = soup.find_all('p', class_='cnnBodyText')
    # print(next_button[1])
    
    # Loop through each element found and extract the 'href' attribute from <a> tags
    for element in elements_with_class:
        a_tag = element.find('a')  # find the first <a> tag within each <p> tag
        if a_tag:
            links.append([a_tag['href']])  # add the 'href' attribute to the list

    url = get_next_url(soup)
    print("pinging " + url + "...")
    response = requests.get(url)

    
filename = "urls.csv"

# Open the file in write mode
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write all rows at once
    writer.writerows(links)