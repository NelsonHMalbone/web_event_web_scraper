import requests
import selectorlib
import CONFIG
import smtplib
from email.message import EmailMessage


URL = "https://programmer100.pythonanywhere.com/tours/"


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
    file_path = "extracted_tour_data.txt"
    with open(file_path, 'a') as file:
        file.write(extracted + "\n")


def read(extracted):
    file_path = "extracted_tour_data.txt"
    with open(file_path, 'r') as file:
        return file.read()


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
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    content = read(extracted)
    # will only send email if a tour is trigger
    if extracted != "No upcoming tours":
        if extracted not in content:
            # only storing and email data when new events spawn
            extracted_data(extracted)
            send_email(message=f'new concert up in coming {extracted}')

