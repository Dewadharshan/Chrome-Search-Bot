import pyautogui
import time
import subprocess
import os
import multiprocessing
import random
import numpy as np
import win32gui
import win32con
import json
from datetime import date


pyautogui.FAILSAFE = False


def generate_random_word():
    global queries
    return random.choice(queries)


def type_query(query):
    for i in query:
        pyautogui.press(i)

        random_number = np.random.normal(50, 40)
        random_number = max(0, min(100, random_number))

        time.sleep(random_number/250)


def search(n):
    for i in range(n):
        search_query = generate_random_word()
        print(f"\tsearched word : {search_query}")

        pyautogui.hotkey('ctrl','k')
        
        type_query(search_query)

        pyautogui.press('enter')

        time_interval = random.uniform(6,8)
        time.sleep(time_interval)


def get_rewards_page():
    pyautogui.hotkey('ctrl','l')
    pyautogui.press('backspace',presses=2)
    pyautogui.typewrite("https://rewards.bing.com/")
    pyautogui.press('enter')


def open_chrome(profile):
    os.startfile(r"E:\\shared folder\\chrome_shortcuts\\"+profile)
    time.sleep(0.5)
    win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_MAXIMIZE)


def close_chrome():
    pyautogui.hotkey('alt', 'f4')


def get_chrome_profile():
    with open(r'E:\\shared folder\\chrome\\search_status_chrome.json', 'r') as status_file:
        search_status = json.loads(status_file.read())
        search_status = search_status['profiles']
    
    profiles = [key for key, value in search_status.items() if value.get("search_count", 0) < 34 and value.get("last_search_time") and (time.time() - value.get("last_search_time")) > 0]
    if profiles == []:
        return None
    return random.choice(profiles)

def verify_search_completion():
    with open(r'E:\\shared folder\\chrome\\search_status_chrome.json', 'r') as status_file:
        search_status = json.loads(status_file.read())
        search_status = search_status['profiles']

    for profile, data in search_status.items(): 
        if data.get("search_count", 0) < 34:
            return False
    
    return True

def update_status_file(current_profile, n_search):
    with open(r'E:\\shared folder\\chrome\\search_status_chrome.json', 'r') as status_file:
        search_status = json.loads(status_file.read())

    search_status['profiles'][current_profile]["search_count"] += n_search
    search_status['profiles'][current_profile]["last_search_time"] = time.time()
    
    with open(r'E:\\shared folder\\chrome\\search_status_chrome.json', 'w') as status_file:
        json.dump(search_status, status_file, indent=4)

def reset_status_file():
    with open(r'E:\\shared folder\\chrome\\search_status_chrome.json', 'r') as status_file:
        search_status = json.loads(status_file.read())

    for profile_data in search_status['profiles'].values():
        profile_data['search_count'] = 0

    with open(r'E:\\shared folder\\chrome\\search_status_chrome.json', 'w') as status_file:
        json.dump(search_status, status_file, indent=4)

with open(r"E:\\shared folder\\queries.txt",'r') as queries:
    queries = queries.read()
    queries = queries.split("\n")
time.sleep(10)

with open(r'E:\\shared folder\\chrome\\search_status_chrome.json', 'r') as status_file:
    status = json.loads(status_file.read())
    
if status['date'] != str(date.today()):
    status['date'] = str(date.today())
    with open(r'E:\\shared folder\\chrome\\search_status_chrome.json', 'w') as status_file:
        json.dump(status, status_file, indent=4)
    reset_status_file()

while True:

    current_profile = get_chrome_profile()

    if current_profile != None:
        print("\n\nCurrent profile : ",current_profile)
        open_chrome(current_profile)
        time.sleep(4)

        n_search = random.randint(1,5)
        print("\tNo of search : ",n_search)
        search(n_search)


        close_chrome()
        update_status_file(current_profile,n_search)

    if verify_search_completion():
        break

    sleep_interval = random.uniform(30,500)
    print("\tsleep time : ",sleep_interval)
    time.sleep(sleep_interval)
