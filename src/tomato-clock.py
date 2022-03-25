'''
# tomato-clock.py
# this is a simple application to arrange your time more properly
# author @NearlyHeadlessJack (https://github.com/NearlyHeadlessJack)
# copyright (c) 2022 N.H.J. on MIT License
# version.2022.03.1030
'''

# import=======================

import time
import os
import json
from pathlib import Path


# =============================

# variables====================

localDate = time.strftime("%Y-%m-%d", time.localtime())
global numClocks,history
numClocks = 1 #经历的番茄钟数量
skipTimes = 0 #跳过的休息次数
cur = 1
clear_command = r'clear' # Linux/macOS
# clear_command = r'cls' # Windows
path_json = r'data.json'
history = {localDate: 0}

# =============================


def ReadJson():
    global numClocks,history
    init_data = {localDate: 0}

    if Path(path_json).exists():
        with open(path_json, "r") as f:
            history = json.load(f)
    else:
        with open(path_json, "w+") as f:
            json.dump(init_data, f,indent=4)
        with open(path_json, "r") as f:
            history = json.load(f)

    if localDate not in history.keys():
        history[localDate] = 0
    
    numClocks = int(history[localDate])
        


# # =============================

def WriteJson():
    global history
    history[localDate] += 1
    with open(path_json, "w+") as f:
        json.dump(history, f,indent=4)

# =============================

ReadJson()
os.system(clear_command)
print ("\033[1;31;40mThis is tomato clock, enjoy studying!\033[0m")
print("\nYou've been learning \033[1;31;40m"+str(numClocks*25)+"\033[0m minutes today!\n")
while cur:
    if input("If you are ready to study, please press \033[1;31;40menter\033[0m!\n") == '':
        numClocks = numClocks + 1
        tB  = time.mktime(time.localtime(time.time()))                    # 记录开始时间
        tC = time.mktime(time.localtime(time.time()))
        while tC-tB <= 25 * 60 - 5:
            tC = time.mktime(time.localtime(time.time()))
            diff = time.gmtime(tC - tB)
            os.system(clear_command)
            print('This is the No.'+ str(numClocks) +' clock!')
            print('{0}  mins  {1} secs remaining!'.format(24-diff.tm_min,59-diff.tm_sec))
            time.sleep(0.98)
        os.system(clear_command)
        print('Congratulations! The No.\033[1;31;40m'+ str(numClocks) + '\033[0m clock is done.')
        print('\nYou can have a rest for \033[1;31;40m'+str(skipTimes * 5 + 5 )+'\033[0m minutes!\n')
        time.sleep(2)
        WriteJson()
        if input("Start resting, please press \033[1;31;40menter\033[0m!\n\
Skip rest (which would be accumulated), please enter the other:\n") == '':
            tB  = time.mktime(time.localtime(time.time()))                    # 记录开始时间
            tC = time.mktime(time.localtime(time.time()))
            breakTime = skipTimes * 5 * 60 + 5 * 60  # accumulate break time
            while tC - tB <= breakTime - 4 :
                tC = time.mktime(time.localtime(time.time()))
                diff = time.gmtime(tC - tB)
                os.system(clear_command)
                print('Rest time!')
                print('{0}  mins  {1} secs remaining!'.format(skipTimes * 5 + 5 - 1 - diff.tm_min, 59 - diff.tm_sec))
                time.sleep(0.98)
            print('\n\nBreak time is done! Clock will re-startup in 4 secs.')
            time.sleep(4)
            skipTimes = 0
            os.system(clear_command) 
        else:
            skipTimes += 1

    else:
        cur = 0
