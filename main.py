import requests
import re
import json
import time
from pprint import pprint
from bs4 import BeautifulSoup


# get first page
# get data about events
# check how many pages are there
# store it to a variable
# iterate over list of pages
# save results to a json file

highest_number = ""
data = []

def get_image_from_a_site(link):
    data = []
    highest_number = []
    
    page = requests.get(link)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        lightbox = soup.find("a", class_="Lightbox")
        try:
            img_link = lightbox["href"]
        except TypeError:
            return None
        return "http://www.kulturalna.warszawa.pl%s" % img_link[1:]

def get_data_from_a_site(link):
    data = []
    highest_number = []
    running = True
    while running:
        try:
            page = requests.get(link)
            running = False
        except requests.exceptions.ConnectionError:
            time.sleep(3)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        soup = soup.find("div", class_="EventsToday")
        soup = soup.find("div", class_="Gut")
        date = ""
        time = ""
        for i in soup:
            if i.name == "h5":
                date = i.get_text()
            if i.name == "dl":
                for j in i:
                    if j.name == "dt":
                        time = j.get_text()
                    if j.name == "dd":
                        links = j.find_all("a")
                        for link in links:
                            my_link = "http://www.kulturalna.warszawa.pl/%s" % link["href"]
                            picture_link = get_image_from_a_site(my_link)
                            if not(picture_link is None):
                                thumbnail_link = picture_link.split(".")
                                thumbnail_link[-2] += "_w180"
                                thumbnail_link = ".".join(thumbnail_link)
                            else:
                                thumbnail_link = "none"
                            data += [{"event": link.get_text().strip(),
                                      "link": my_link,
                                      "date": date.strip(),
                                      "time": time.strip(),
                                      "picture": picture_link,
                                      "thumbnail": thumbnail_link}]
        pager = soup.find("div", class_="Pager").find_all("a")
        for i in pager:
            try:
                highest_number += [int(i.get_text())]
            except ValueError:
                pass
        highest_number = sorted(highest_number)
        highest_number = highest_number[-1]
        pprint(data)
        return (data, highest_number)

data_i, highest_number_i = get_data_from_a_site("http://www.kulturalna.warszawa.pl/wydarzenia,,,,,,,,,,,,,,,1,1.html")
data += list(data_i)
highest_number = highest_number_i

for i in range(2, highest_number):
    data_i, highest_number_i = get_data_from_a_site("http://www.kulturalna.warszawa.pl/wydarzenia,,,,,,,,,,,,,,,1,%s.html" % i)
    data += data_i

with open("output.json", "w") as f:
    f.write(json.dumps(data))

pprint(data)
print(highest_number)