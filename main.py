import sys
import time

import keyboard
import requests
import selectorlib
import CONFIG
import smtplib
from email.message import EmailMessage
import sqlite3


URL = "https://programmer100.pythonanywhere.com/tours/"

# Establishg a connection along with a cursor
connection = sqlite3.connect('data.db')


# scraping the url provided
def scrape(url):
    """Scrape the page source from the url"""
    response = requests.get(url)
    text_source = response.text
    return text_source


# extracting the text source that we get from the request response
def extract(text_source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(text_source)["tours"]
    return value


# placing extracted data on to a txt file
def extracted_data(extracted):
    # used for txt files and such
    #now = time.strftime("%a, %d %b %Y %H:%M:%S ")
    #file_path = "extracted_tour_data.txt"
    #with open(file_path, 'a+') as file:
        #file.write(now + extracted + "\n")

    # striping ","
    row = extracted.split(",")
    # striping leading and trailing empty space
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    # using this because we expect one list at a time
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()
def read(extracted):
    # storing data with txt
    #file_path = "extracted_tour_data.txt"
    #with open(file_path, 'r') as file:
        #return file.read()
    # setting up for sql data base
    # striping ","
    row = extracted.split(",")
    # striping leading and trailing empty space
    row = [item.strip() for item in row]
    band, city, date = row
    # query data based on condition
    cursor = connection.cursor()
    # asking our database to give us all rows where band is band and such
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                   (band, city, date))
    row = cursor.fetchall()
    print(row)
    return row

# will send a email for new or upcoming events
def send_email(message):
    print("send_email function has started")
    username = CONFIG.key_user_sender
    password = CONFIG.key_pass

    receiver = CONFIG.key_user_reciever
    email_message = EmailMessage()
    email_message["Subject"] = "New Tour Alert!"
    email_message.set_content("Hey, we just had a new tour event pop up")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(username, receiver, message)
        server.quit()
    print("Email was Sent")

# reading the file to beable to tell if a email needs to be sent


if __name__ == "__main__":
    print("Press and hold Esc to quit program")
    while True:
        try:
            scraped = scrape(URL)
            extracted = extract(scraped)
            print(extracted)
            #content = read(extracted) used for txt and such
            # will only send email if a tour is trigger
            if extracted != "No upcoming tours":
                # only diffent when "No upcoming tours"
                row = read(extracted)
                #if extracted not in content: only for txt and such
                if not row: # checking for no such rows then we store into data base
                    # only storing and email data when new events spawn
                    extracted_data(extracted)
                    send_email(message=f'new concert up in coming {extracted}')
            time.sleep(3)

            if keyboard.is_pressed("Esc"):
                print("Come Back tomorrow to see more events")
                sys.exit(0)
        except:
            break