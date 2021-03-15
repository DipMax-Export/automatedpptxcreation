import asyncio
from Procedure import procedure
from crawling.Crawl_simple import Crawl_simple
from inputs import inputs
import time
from os.path import expanduser
import multiprocessing
from crawling.ApiCall import ApiCall

# Settings
home = expanduser("~")
usr_i = dict()

q = multiprocessing.Queue() # Stores the links and the api responses

# run apicall
def task1(loop,links,q,page) -> None:

    if page == "m":
        loop.run_until_complete(asyncio.gather(ApiCall(links,q)))
    else:
        loop.run_until_complete(asyncio.gather(Crawl_simple(links,q)))

def task2(loop,q,usr_i) -> None:
    loop.run_until_complete(asyncio.gather(procedure(q,usr_i)))

def async_main() -> None:

    usr_i = inputs()
    links = usr_i["links"]
    page = usr_i["page"]
    loop = asyncio.get_event_loop()
    loop2 = asyncio.get_event_loop()

    # Two process 1 for the asynchronous API calls and 1 for the creation of the presentations
    p1 = multiprocessing.Process(target=task1, args=(loop, links,q,page))
    p2 = multiprocessing.Process(target=task2, args=(loop2,q,usr_i))

    # creating thread
    p1.start()
    p2.start()


    p1.join()
    p2.join()

async_main()

