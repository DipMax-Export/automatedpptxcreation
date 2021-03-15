
from os.path import expanduser
home = expanduser("~")

def inputs():
    # Single or multiple file
    links = []
    input_link = ""
    d_inputs = {}

    while True:
        count_files = input("Do you want to read in one(o) or many(m) links?\n")
        if count_files == "o":
            input_link= input("Please provide me with the link:\n")
            links.append(input_link)
            d_inputs["links"] = links
            break
        if count_files == "m":
            link_list_path = input("Please provide the path to the file with the links:\n")
            #Read in of links
            with open(link_list_path) as file:
                for line in file:
                    if not line.startswith("https://"): continue
                    if "mobile" in line:
                        links.append(line.strip() + "&lang=en")
                    else:
                        links.append(line.strip())
            d_inputs["links"] = links
            break
        else:
            print("Please choose between o and m")

        # Russia or Bangladesh
    while True:
        tgt_curr = input(
            "Please select Russia or Bangladesh for the price calculation by r for Russia and b for Bangladesh\n")
        if tgt_curr == "r":
            d_inputs["tgt_curr"] = "RUB"
            d_inputs["folder_path"] = home + "/Dropbox/DipMax/Exportländer/Russland/Neu"
            break
        elif tgt_curr == "b":
            d_inputs["tgt_curr"] = "BDT"
            d_inputs["folder_path"] = home + "/Dropbox/DipMax/Exportländer/Bangladesh/Neu"
            break
        else:
            print("Please choose between r and b")
            break
    # Zuschlag
    while True:
        margin = input("Please give a surcharge for the price in %!\n")
        if 0 <= int(margin) <= 100:
            d_inputs["margin"] = margin
            break
        else:
            print("Please add a value between 0 and 100 %")

    # Mobile.de oder ev-database
    while True:
        page = input("Please choose mobile.de(m) or ev-database(e)\n")
        if page == "m":
            d_inputs["page"] = "m"
        else:
            d_inputs["page"] = "e"
            d_inputs["folder_path"] = home + "/Dropbox/DipMax/Exportländer/Bangladesh/ElectroPortofolio"
        break

    return d_inputs
