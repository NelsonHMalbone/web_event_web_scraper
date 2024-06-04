import requests
import selectorlib


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


# will send a email for new or upcoming events
def send_email():
    print("Email was sent")


# reading the file to beable to tell if a email needs to be sent
def read(extracted):
    file_path = "extracted_tour_data.txt"
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    content = read(extracted)
    print(extracted)
    # will only send email if a tour is trigger
    if extracted != "No upcoming tours":
        if extracted not in content:
            # only storing and email data when new events spawn
            extracted_data(extracted)
            send_email()

