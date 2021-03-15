import re

from bs4 import BeautifulSoup


def CrawlEV_database(doc, link, home):
    car_specs = {}
    car_specs["Name"] = doc.find_all("h1")[0].text

    range = doc.find_all(id="range")

    for element in range:
        trs = element.find_all("tr")
        for tr in trs:
            td = tr.findChildren("td")
            if not td:
                continue
            if "City - Mild Weather" in td[0].text:
                car_specs["City"] = td[1].text
            if "Highway - Mild Weather" in td[0].text:
                car_specs["Highway"] = td[1].text

    performance = doc.find_all(id="performance")

    for element in performance:
        trs = element.find_all("tr")
        for tr in trs:
            td = tr.findChildren("td")
            if not td:
                continue
            if "Acceleration" in td[0].text:
                car_specs["Acceleration"] = td[1].text.split(".")[0] + " sec (0-100 km/h)"
            if td[0].text == "Top Speed":
                car_specs[td[0].text] = td[1].text

    charging = doc.find_all(id="charging")

    for element in charging:
        trs = element.find_all("tr")
        for tr in trs:
            td = tr.findChildren("td")
            if not td:
                continue
            if "Battery Useable" in td[0].text:
                car_specs["Battery Useable"] = td[1].text
            if "Charge Power" in td[0].text:
                car_specs["Charge Power"] = td[1].text
            if "Charge Time" in td[0].text:
                car_specs["Wall box"] = td[1].text.split(" ")[0] + "h"
            if "Fastcharge Power" in td[0].text:
                car_specs[td[0].text] = td[1].text
            if "Fastcharge Time" in td[0].text:
                car_specs["Station"] = td[1].text
            if "Charge Speed" in td[0].text:
                car_specs["Wall box"] = car_specs["Wall box"] + ", " + td[1].text
            if "Fastcharge Speed" in td[0].text:
                car_specs["Station"] = car_specs["Station"] + ", " + td[1].text

    charging_time = doc.find_all(class_="charging-table-standard")

    for element in charging_time:
        trs = element.find_all("tr")
        for tr in trs:
            td = tr.findChildren("td")
            if not td:
                continue
            if "Wall Plug" in td[0].text:
                car_specs["Wall Plug"] = td[3].text + ", " + td[4].text

    price_charge = float(car_specs["Battery Useable"].split(" ")[0]) * 7.78

    car_specs["Full charge"] = str(int(price_charge)) + " BDT"

    dimensions = doc.find_all(class_="data-table")
    for element in dimensions:
        trs = element.find_all("tr")
        for tr in trs:
            td = tr.findChildren("td")
            if not td:
                continue
            if "Length" in td[0].text:
                car_specs[td[0].text] = td[1].text
            if "Width" in td[0].text:
                car_specs[td[0].text] = td[1].text
            if "Height" in td[0].text:
                car_specs[td[0].text] = td[1].text
            if "Weight Unladen" in td[0].text:
                car_specs["Weight Unladen"] = td[1].text
            if "Seats" in td[0].text:
                car_specs["Number of Seats"] = td[1].text.split(" ")[0]
            if "Car Body" in td[0].text:
                car_specs["Category"] = td[1].text

    pricing = doc.find_all(id="pricing")
    for element in pricing:
        trs = element.find_all("tr")
        for tr in trs:
            td = tr.findChildren("td")
            if not td:
                continue
            if "United Kingdom" in td[0].text:
                car_specs["price"] = td[1].text
                if len("".join(filter(str.isdigit, car_specs["price"]))) != 0:
                    break
            if "Germany" in td[0].text:
                car_specs["price"] = td[1].text
                break

    a = doc.find_all('a')
    for href in a:
        if "/img/auto/" in href.attrs['href']:
            img = href.attrs['href']
            break

    car_specs["img"] = "https://ev-database.org" +img

    car_specs["link"] = link

    return car_specs