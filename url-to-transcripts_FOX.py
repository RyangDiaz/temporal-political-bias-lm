from bs4 import BeautifulSoup
import requests
import json
import csv

def save_article(response, date):
    with open("transcripts_tucker/" + date + ".txt", 'w', encoding='utf-8') as file:
            
        soup = BeautifulSoup(response.text, 'html.parser')

        specific_content = soup.select_one('html body div div div div div main article div div div p:nth-of-type(2)').text
        file.write(specific_content)
    print(date)

with open("../csv_files/tucker_urls.csv", 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    #headers = next(reader)

    for row in reader:
        print(row)

        url = "https://www.foxnews.com/" + row['\ufeffurl']
        
        response = requests.get(url)
        if response.status_code == 200:
            save_article(response, row['date'])

