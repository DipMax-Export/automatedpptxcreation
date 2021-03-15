import asyncio
import sys
import threading

from crawling.CrawlCarPhotos import CrawlCarPhotos
from crawling.CrawlCarSpecs import CrawlCarSpecs
from crawling.CrawlEv_database import CrawlEV_database
from presentation.CreatePptx import CreatePptx
from util.CreateFolder import CreateFolder
from util.Api_Pptx_To_Png import Pptx_To_Png
from util.PriceCalculation import PriceCalculation
from util.SaveImgLinktoFile import SaveImgLinktoFile
from util.SaveImgtoFile import SaveImgtoFile
from util.WriteCarSpectoFile import WriteCarSpectoFile
from bs4 import BeautifulSoup
import os
from os.path import expanduser
import uuid

# Settings
home = expanduser("~")


async def get_png_url(pptx_output):
    png_url = Pptx_To_Png(pptx_output)  # Call api to create png
    return png_url


async def get_user_ok():
    while True:
        pptx_correct = input("PPTX was created. Please check if everything is correct and type y\n")
        try:
            if pptx_correct == "y":
                return pptx_correct
                break
        except:
            print("Please type y and enter!")
            continue

async def ainput():
    loop = asyncio.get_event_loop()
    fut = loop.create_future()
    def _run():
        print("PPTX was created. Please check if everything is correct and type y\n")
        line = sys.stdin.readline()
        loop.call_soon_threadsafe(fut.set_result, line)
    threading.Thread(target=_run, daemon=True).start()
    return await fut

async def console_input_loop():
    while True:
        inp = await ainput()
        return f"[{inp.strip()}]"

async def procedure(q, usr_i):
    count = 1
    while True:
        if not q.empty():
            lis_with_resp_a_li = q.get()
            link = lis_with_resp_a_li[0]
            response = lis_with_resp_a_li[1]
            last_link = lis_with_resp_a_li[2]

            # Parse html
            doc = BeautifulSoup(response, 'html.parser')
            if doc.find_all("div", {"class": "vip-error__title"}) != []:
                continue
            if doc.title.string == "Ups, bist Du ein Mensch? / Are you a human?":
                with open("/home/maxsofr/Dropbox/DipMax/Exportländer/failed_apicall.txt", "a") as file:
                    file.write(link + "\n")
                continue

            if usr_i["page"] == "m":
                car_specs = CrawlCarSpecs(doc, link, home)
                pic_list = CrawlCarPhotos(doc)
                print("Pictures Check")
                # Price calculation
                if car_specs["net_price:"] == car_specs["price:"]:
                    price = car_specs["price:"]
                else:
                    price = car_specs["net_price:"]
                prices = PriceCalculation(price, usr_i["tgt_curr"], usr_i["margin"])
            else:
                car_specs = CrawlEV_database(doc, link, home)
                pic_list = []
                pic_list.append(car_specs["img"])
                # Price
                prices = PriceCalculation(car_specs["price"], usr_i["tgt_curr"], usr_i["margin"])
            print("CarSpecs Check")

            car_path = os.path.join(usr_i["folder_path"], car_specs["Name"] + " " + str(uuid.uuid1().hex))

            # Create folder
            CreateFolder(car_path)

            # Persist CarSpecs and Link in CarSpecs file
            WriteCarSpectoFile(car_path, car_specs)

            # Crawl carPhoto and persist links in linkList and persist photo
            img_path = SaveImgtoFile(pic_list[0], os.path.join(car_path, car_specs["Name"]))
            SaveImgLinktoFile(car_path, pic_list)



            # Create presentation
            pptx_output = CreatePptx(car_specs, img_path, car_path, prices, home, usr_i["page"])

            await console_input_loop()

            png_url = await get_png_url(pptx_output)
            SaveImgtoFile(png_url, os.path.join(car_path, car_specs["Name"]))

            count += 1
            print("Operation for "
                  + car_specs["Name"]
                  + " successful! There are "
                  + str(count) + " left from " + str(len(usr_i["links"])) + " links")

            # End of code
            if last_link:
                print("Done")
                break
