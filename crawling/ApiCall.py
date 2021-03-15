#  Install the Python Requests library:
# `pip install requests`
import requests


async def get_response(element):
    response = requests.get(
        url="https://app.scrapingbee.com/api/v1/",
        params={
            "api_key": "X0ZT9J9CHAQRQ6J3VQSPOD9AEPMDASMKICSDX2I2O37JXQHU1KREOBGL51U70UMJ82S64MIR4TQM7CF1",
            "url": element,
        },
    )
    return response


async def ApiCall(links,q):
    count = 0
    for element in links:
        if count == len(links)-1: #Last Link
            response = await get_response(element)
            q.put([element, response.text,True])
        else:
            response = await get_response(element)
            q.put([element, response.text,False])
        print("No. " + str(links.index(element)))
        count += 1

