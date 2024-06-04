import requests
import selectorlib


URL = "https://programmer100.pythonanywhere.com/tours/"

def scrape(url):
    """Scrape the page source from the url"""
    response = requests.get(url)
    text_source = response.text
    return text_source


def extract(text_source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(text_source)["tours"]
    return value


def extracted_data(extracted):
    file_path = "extracted_tour_data.txt"
    with open(file_path, 'a') as file:
        file.write(extracted + "\n")


def send_email():
    print("Email was sent")

def read(extracted):
    file_path = "extracted_tour_data.txt"
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    extracted_data(extracted)
    content = read(extracted)
    print(extracted)
    # will only send email if a tour is trigger
    if extracted != "No upcoming tours":
        if extracted not in content:
            send_email()

