# All the library imports we need
import requests
from bs4 import BeautifulSoup
import time
import datetime
import os

# Function to search for text in a webpage
def search_text_in_webpage(url, search_text):
    response = requests.get(url)
    # library to parse webpage
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all anchor tags in the page
    links = soup.find_all('a')
    
    # Search for the text in the links
    for link in links:
        # compare to current chapter
        if link.string and search_text in link.string:
            return link.get('href')  # Return the URL of the found link
    return None

# function to send message in discord
def send_discord_message(webhook_url, message):
    data = {
        'content': message
    }
    response = requests.post(webhook_url, json=data)
    
    if response.status_code == 204:
        print("Message sent to Discord channel!")
    else:
        print("Failed to send message. Status code:", response.status_code)

# start of main function
if __name__ == '__main__':
    starting_url = 'https://tcbscans.me'
    # read in memory
    file_path = os.path.join("/home/donbox/OnePieceScanner/", "currentchapter.txt")
    with open(file_path, "r") as file:
        text_to_search = file.readline()
        file.close()
    discord_webhook_url = 'https://discord.com/api/webhooks/1296498010418843680/klvCKRVYAbtH52tbWnvVefhdTtHRkFvowOsYXUYN65FjP_zONO9GwrQ4bayGq2YJx2ay'
    custom_message = '<@&1146944344264282142> <@&1146944344264282142> <@&1146944344264282142> ITS HERE LETS GOOOOOOOOOOO!!!!!!!!!!!!!!!!!!!!!'

# needed converts so that current chapter string is comparable to links on tcbscans
temp = int(text_to_search)
text_to_search = str(temp)

# starts the infinite loop
chapter_released = 1

while chapter_released:
    # first function call to search the links
    found_url = search_text_in_webpage(starting_url, text_to_search)
    print(f"searching for {text_to_search}")
    if found_url:
        # append url directory location to tcbscans url
        new_url = starting_url + found_url
        print(f"Its Out!!!!!!!!!!!!!!!: {new_url}")
        # second function calls to send discord messages
        send_discord_message(discord_webhook_url, new_url)
        send_discord_message(discord_webhook_url, custom_message)
        # convert to int to add 1 to the chapter and convert back to string to save in memory
        current_chapter = int(text_to_search)
        current_chapter += 1
        print(f"Now searching for chapter {current_chapter}")
        text_to_search = str(current_chapter)
        with open(file_path, "w") as file:
            file.write(text_to_search)
            file.close()
    else:
        # chapter not found, wait 10 seconds and run restart looking
        time.sleep(10)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Still not out...........{timestamp}")