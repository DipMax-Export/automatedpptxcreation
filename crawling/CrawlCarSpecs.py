import re

from bs4 import BeautifulSoup


def CrawlCarSpecs(doc, link, home):
    global fuel_consumption, mileage, price, net_price
    car_specs = {}

    with open(home + "/Dropbox/DipMax/Code/Fields_from_td.txt", "r") as file:
        for line in file:
            splitted = line.strip().split(";")
            car_specs[splitted[0]] = splitted[1]

    for key, value in car_specs.items():
        if key == "Fuel Consumption:" or key == "link" or key == "Condition:":
            continue
        else:
            if doc.select(value) != []:
                for element in doc.select(value):
                    if value == "#rbt-ad-title": # Car name
                        title_split = element.text.split(" ")
                        title_split = title_split[0] + " " + title_split[1]
                        car_specs[key] = title_split
                    elif value == "#rbt-category-v": # Car category
                        if "SUV" in element.text:
                            car_specs[key] = "SUV"
                        else:
                            car_specs[key] = element.text
                    elif value == "#rbt-cubicCapacity-v": # Engine
                        cubic_capacity = ''.join(filter(str.isdigit, element.text))
                        car_specs[key] = cubic_capacity + " cc"
                    elif value == "#rbt-transmission-v": # Gear box
                        if "Automatic" in element.text:
                            car_specs[key] = "Automatic"
                        elif "Manual" in element.text:
                            car_specs[key] = "Manual"
                    elif value == "#rbt-firstRegistration-v": # year of manufacturing
                        year_of_manufacturing = re.findall("\d+$", element.text)
                        car_specs[key] = year_of_manufacturing[0]
                    elif value == "#rbt-mileage-v": # Kilometer
                        mileage = ''.join(filter(str.isdigit, element.text))
                        car_specs[key] = '{:20,.0f}'.format(int(mileage)).lstrip() + " km"
                    elif value == "#rbt-pt-v": # price
                        price = ''.join(filter(str.isdigit, element.text))
                        car_specs[key] = price
                    elif value == ".rbt-sec-price": # net_price
                        net_price = ''.join(filter(str.isdigit, element.text))
                        car_specs[key] = net_price
                    else:
                        car_specs[key] = element.text # Basic Fuel Type, Number of Seats, Color, Interior Design
            else:
                car_specs[key] = "N/A"
    # Fuel consumption
    if doc.find_all("div", {"id": "rbt-envkv.consumption-v"}) == []:
        fuel_consumption = "0.0"
    for element in doc.find_all("div", {"id": "rbt-envkv.consumption-v"}):
            fuel_consumption = element.select_one(".u-margin-bottom-9").text.split(" ")[0]
            fuel_consumption = re.findall("[0-9]+", fuel_consumption)
            fuel_consumption = fuel_consumption[0] + "." + fuel_consumption[1]
    car_specs["Fuel Consumption:"] = fuel_consumption + "l/100km (comb.)"

    # Co2 Efficiency
    if car_specs["CO₂ efficiency:"] == "#rbt-envkv.efficiencyClass-v":
        car_specs["CO₂ efficiency:"] = "A"

    # Conditions
    if int(mileage) < 1000:
        car_specs["Condition:"] = "new"
    elif int(mileage) > 1000:
        car_specs["Condition:"] = "used"

    # Price
    if car_specs["net_price:"] == "N/A":
        car_specs["net_price:"] = price

    car_specs["link"] = link
    return car_specs

# Um später mit Pfund, umzugehen
# elif "£" in splitted[1]:
#   price = ''.join(filter(str.isdigit, splitted[1]))
#  price = (int(price)) / 1.20 * Curr_GB_EUR
# price = price + price * fee_curr_ex + fee_GB
##data[splitted[0]] = price
# elif "€" in splitted[1]:
#   price = ''.join(filter(str.isdigit, splitted[1]))
#  data[splitted[0]] = price

# with open("/home/maxsofr/Dropbox/DipMax/Code/bad_response.txt", "r") as file:
#     doc = file.read()
#     link = "link"
#     home = "/home/maxsofr/"
#
# doc = BeautifulSoup(doc, 'html.parser')
#
#
# if doc.select("#rbt-pt-v") == []:
#     with open("/home/maxsofr/Dropbox/DipMax/Exportländer/failed_links.txt", "a") as file:
#         file.write(link + "\n")
#         print("sorry")
# else:
#     print(CrawlCarSpecs(doc, link, home))




