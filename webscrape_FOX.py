from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

#thanks chatgpt
def get_past_sundays(n):
    """
    Generates dates for the past 'n' Sundays from the last Sunday.
    
    Args:
    - n (int): Number of Sundays to generate.
    
    Returns:
    - List of strings representing the dates of past Sundays in the format "month-day-year".
    """
    # Current date
    now = datetime.now()
    
    # Find last Sunday
    last_sunday = now - timedelta(days=(now.weekday() + 1) % 7)
    
    # Generate a list of past Sundays
    sundays = [(last_sunday - timedelta(weeks=i)).strftime("%B-%d-%Y").lower() for i in range(n)]
    
    # Format the dates correctly (month in lowercase, hyphens for separation)
    formatted_sundays = [date.replace(" ", "-") for date in sundays]
    
    return formatted_sundays

def save_article(response, date):
    with open("transcripts_FOX/" + date + ".txt", 'w') as file:
            
        soup = BeautifulSoup(response.text, 'html.parser')

        specific_content = soup.select_one('html body div div div div div main article div div div p:nth-of-type(2)').text
        file.write(specific_content)
    print(date)


# Get the list of Sundays
past_sundays = get_past_sundays(2000)

# Print the dates
for date in past_sundays:
    print(date)
    url = 'https://www.foxnews.com/transcript/fox-news-sunday-' + date
    url_alt = 'https://www.foxnews.com/transcript/fox-news-sunday-on-' + date
    response = requests.get(url)
    response_alt = requests.get(url_alt)
    if response.status_code == 200:
        save_article(response, date)
    elif response_alt.status_code == 200:
        save_article(response_alt, date)
    else:
        #print(date + " does not have a transcript")
        #print("error codes: " + str(response.status_code) + " " + str(response_alt.status_code))
        
