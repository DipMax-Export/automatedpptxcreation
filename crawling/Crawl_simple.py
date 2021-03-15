
import requests

async def Crawl_simple(links,q):
    count = 0
    for element in links:
        if count == len(links) - 1:  # Last Link
            response = requests.get(element)
            q.put([element, response.text, True])
        else:
            response = requests.get(element)
            q.put([element, response.text, False])
        print("No. " + str(links.index(element)))
        count += 1