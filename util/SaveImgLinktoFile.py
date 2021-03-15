import os

def SaveImgLinktoFile(car_path, pic_list):
    f = open(os.path.join(car_path,"pic_list.txt"), "w+")
    for element in pic_list:
        f.write(element + "\n")

    f.close()