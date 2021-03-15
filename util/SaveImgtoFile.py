import urllib.request


def SaveImgtoFile(img_url, save_path):
    url = img_url
    r = urllib.request.urlopen(url)
    with open(save_path + ".png", "wb") as f:
        f.write(r.read())

    return save_path + ".png"