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

def send_email():
    print("Email was sent")
if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    if extracted != "No Upcoming Tours":
        send_email()

