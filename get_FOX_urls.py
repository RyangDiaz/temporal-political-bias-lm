from bs4 import BeautifulSoup
import requests
import json
import csv

#xpath: /html/body/pre/text()

# Print the dates

with open("../csv_files/articles2.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["title", "url", "date", "id"])

    for i in range(10000):
        url = "https://www.foxnews.com/api/article-search?searchBy=categories&values=fox-news%2Ftranscript&size=30&from=" + str(i*30 + 9901)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup)
        
        if response.status_code == 200:
            #pre_tag = soup.find('pre')
            data = json.loads(str(soup))
            for j, article in enumerate(data):
                print("writing " + article["title"])
                writer.writerow([article["title"], article["url"], article["publicationDate"], 9901 + i*30 + j])
            
        else:
            print("Error: Page not found.")
            #print(date + " does not have a transcript")
            #print("error codes: " + str(response.status_code) + " " + str(response_alt.status_code))
        
