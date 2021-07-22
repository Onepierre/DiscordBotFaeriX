import pickle
import time
import shutil
import requests
import numpy as np
from random import *
import os
import random

def get_image(url, name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open("cartoons/cardboard_crack/"+name+".jpg", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        print("Error " + str(r.status_code))
        print("url was: " + url)
    return "cartoons/cardboard_crack/"+name+".jpg"

def download_post(url):
    r = requests.get(url)
    if r.status_code == 200:
        splitted_text = 1
        splitted_text = r.text.split('"')
        url_out = None
        for a in splitted_text:
            if not "=" in a and "http" in a and "\/" not in a and not ".pnj" in a:
                if "64.media.tumblr" in a:
                    url_out = a
                    if "_500" in a or "s500x750" in a or "_400" in a:
                        if ".gifv" in a or ".jpg" in a:
                            break

        if not url_out == None:
            temp = url.split("/")

            date = r.text.split('''time datetime''')[1][2:12]
            name = date + "_" + temp[-1] + "_" + temp[-2]
            file = get_image(url_out, name)
            print("Download successful")
    else:
        print("Error " + str(r.status_code))
        print("url was: " + url)
    return name,file

def get_links():
    url_base = "https://cardboard-crack.com/"
    link_list = []
    for page_counter in range(1, 2):
        url = url_base+"page/" + str(page_counter)
        time.sleep(0.1)
        r = requests.get(url)
        if r.status_code == 200:
            splitted_text = r.text.split('"')
            for a in splitted_text:
                if "https://cardboard-crack.com/post/" in a and "#notes" not in a and "tumblr" not in a:
                    link_list.append(a)
        else:
            print("Error " + str(r.status_code))
            print("url was: " + url)

    link_list = np.array(link_list)
    link_list = np.unique(link_list)
    return link_list


if __name__ == "__main__":
    1
