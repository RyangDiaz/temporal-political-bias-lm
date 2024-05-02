from bs4 import BeautifulSoup
import requests
import json
import csv

def save_article(response, date):
    with open("transcripts_lemon/" + date + ".txt", 'w') as file:
            
        soup = BeautifulSoup(response.text, 'html.parser')

        # specific_content = soup.select_one('html body div:nth-of-type(2) div:nth-of-type(1) div div div:nth-of-type(1) div:nth-of-type(2) table tbody tr:nth-of-type(2) td div p:nth-of-type(6)').text
        elements_with_class = soup.find_all('p', class_='cnnBodyText')

        # Print each element found
        #print(elements_with_class[2].text)
        file.write(elements_with_class[2].text)
    print(date)

def extract_date(url):
    parts = url.split('/')

    # The date is located at the index where 'date' is found plus one
    date_index = parts.index('date') + 1
    date_str = parts[date_index]

    return date_str

with open("../csv_files/lemon_urls.csv", 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    #headers = next(reader)

    for row in reader:
        #print(row)

        url = "https://transcripts.cnn.com" + row['url']
        
        response = requests.get(url)
        if response.status_code == 200:
            save_article(response, extract_date(row['url']))
        else:
            print(url + " not found")

