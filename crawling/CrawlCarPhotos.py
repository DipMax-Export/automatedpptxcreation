
def CrawlCarPhotos(doc):

    i = 0
    id_generic = "rbt-gallery-img-" + str(i)
    pic_list = []
    for element in doc.find_all("div", {"id": id_generic}):
        if element.select_one("img").attrs["src"]:
            pic_list.append("https://" + element.select_one("img").attrs["src"][2:])
            break
    i = 1
    while doc.find("div", {"id": id_generic}) != None:
        id_generic = "rbt-gallery-img-" + str(i)
        for element in doc.find_all("div", {"id": id_generic}):
            if element.select_one(".slick-loading") != None and element.select_one(".slick-loading").attrs["data-lazy"]:
                pic_list.append("https://" + element.select_one(".slick-loading").attrs["data-lazy"][2:])
                break
        i += 1

    return pic_list
