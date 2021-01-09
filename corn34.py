#! /usr/bin/env python3

import csv
import os
import platform
import re
import sys
from sys import argv as argument_val
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import check_valid as check


options = ["-help", "-start", "-tags"]
common_use = "http://rule34.xxx/index.php?page=post&s=list&tags="
version = "0.1.0"

def main():
    if argument_val[1].lower() not in options:
        print("Command not found, use <-help> command if you need support.")
    else:
        if argument_val[1].lower() == "-start":
            start()
        elif argument_val[1].lower() == "-tags":
            showlist()
        else:
            print(help())

def replaceBlank(str):
    if " " in str:
        return (str.replace(" ", "_"))
    else:
        return str



def help():
    return """
        To get yourself a FRESH CORN easily and awesomely, 
        you should, and would like to acknowledge these useful commands.

        -start:
            Using this command, of course, you'll get started with your wonderful crawling experience.
            At the beginning, you will be asked for inserting the MAIN TAG.
            MAIN TAG could be anything - As long as Rule 34 exists.
            You can get started by searching Artist's / Character's Name, or A Category.

            Next, you will be asked for inserting some Additional Tag(s).
            This is an optional data, you can feel free to leave it empty, literally.
            Also, add a \"-\" could make your insert tag became A Negative Tag,
            you can use it when trying to disable the categories you don't like to see.

            You can also learn the commonly used tags by using <-tags> command. 

        -tags :
            Using this command, the most commonly used / not used will show in this window.
            You can use it when you have no idea.


    """

def start():
    #Yeah, i know multiple return isn't a good practice...
    main_tag, get_url = inputMainTag()
    get_url = inputAdditionalTag(get_url)
    confirm = input("\nFinally, the url will be like: %s \nConfirm? (Leave it empty if False)..." %get_url).lower() or "no"
    if (confirm != "no"):
        # Process:
        # Find the last page -> set it as the goal and start running crawler process
        # -> download all of the links that exist in saved_links[]
        main_tag = check.overwrite_invalid(main_tag)
        # do it in order to prevent FileNotFound Error
        
        last_page = get_lastPID(get_url)
        saved_links = launchCrawler(get_url, last_page)
        download(saved_links, main_tag)
    else:   sys.exit()

def showlist():
    return "LIIIIIIIIST"

# =====

def inputMainTag():
    #return the first concated url
    try:
        main_tag = input("Let's get started from the MAIN TAG, should we? (Empty for exit)...").lower() or "no"
        if (main_tag == "no"):
            sys.exit()
        else:
            return_url = common_use + replaceBlank(main_tag)
            return main_tag, return_url
    except(SyntaxError, ValueError, UnicodeDecodeError):
        print(sys.exc_info()[0], " occured! Make sure if you're typing it well.")        

# =====

def inputAdditionalTag(rule34page):
    running = True
    add_array = [] 

    while(running):
        try:
            additional_tag = input("Insert the Additional Tags: (Leave it empty if None)...").lower() or "no"
            if (additional_tag == "no"):
                running = False
            else:
                if (additional_tag not in add_array):
                    add_array.append(additional_tag)
                else:
                   print("Tag exists! Please insert other tag.")
        except(SystemError, ValueError, UnicodeDecodeError):
            print(sys.exc_info()[0], " occured! Make sure if you're typing it well.")
            running = False

    for elem in add_array:
        elem = "+" + replaceBlank(elem)
        rule34page += elem

    return rule34page

# =====

def get_lastPID(get_url):
    # TODO : If only ONE page??
    #Default : Until the last page
    try:
        request = requests.get(get_url)
        soup = BeautifulSoup(request.text, "lxml")
        find_last_page = soup.find("div", class_ = "pagination").find("a", alt="last page")["href"]
        
        regulation = re.compile(r"\d+")
        lastPID = regulation.search(find_last_page)
        result = int(lastPID.group())//42 + 1

        return result
    except(AttributeError, TypeError):
        return 1
         #return the page number "1" if beautifulsoup return EMPTY

# =====

def download(saved_links, main_tag):
    try:
        if not os.path.exists(main_tag  ):
            os.mkdir(main_tag)
        else:
            main_tag = main_tag + "(alter)"
            os.mkdir(main_tag)

        index = 0
        for sauce in tqdm(saved_links):
            img = requests.get(sauce)

            with open(main_tag + "\\" + main_tag + str(index) + ".png", "wb") as file:
                file.write(img.content)
            index += 1

        print("...Complete!")
    except:
        print(sys.exc_info()[0])
        sys.exit()

# =====
def launchCrawler(current_page, last_page):
    basePID = 0
    saved_links = []

    for i in range(last_page):
        print("You're now at:", current_page)
        print("=================================================")

        request = requests.get(current_page)
        soup = BeautifulSoup(request.text, "lxml")
        # ---"If you can, I recommend you install and use lxml for speed."
        found = soup.select("div.content div span.thumb a")

        for elem in found:
            download = "http://rule34.xxx/" + elem["href"]
            download_request = requests.get(download)
            download_soup = BeautifulSoup(download_request.text, "lxml")
            result = download_soup.find("div", class_="content").find("img")["src"]
            
            if (result == "https://rule34.xxx/images/shirt2.jpg"):
                pass
            else:
                print(result)
                saved_links.append(result)

        print("=================================================")
        basePID += 42
        nextpage = current_page + "&pid=" + str(basePID)
        current_page = nextpage

    return saved_links

if __name__ == "__main__":
    # check python version at beginning
    major = sys.version_info[0]
    minor = sys.version_info[1]
    micro = sys.version_info[2]

    python_ver = str(major)+"."+str(minor)+"."+str(minor)

    if (major != 3 or (major == 3 and minor < 6)):
        print("Corn34 requires Python3.6+, your version is ", python_ver, 
            "\nVisit Python's official website and upgrate it before getting started.")
        sys.exit(1)
    
    main()