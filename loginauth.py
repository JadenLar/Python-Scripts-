import requests
from bs4 import BeautifulSoup
import cfscrape
import re

from numpy import array

cookies = {
    'ips4_IPSSessionFront': '1mdjcf2rvhdoc0upmhvjkcm0l4',
    '__stripe_mid': 'c87e7271-a75f-44b8-9568-dcd3a134c6e44fc640',
    'cf_clearance': '8Id6Si0fCx2aj.eUyKTa.IoGZpPVFOVFqoPY1iH.D5g-1656182299-0-150',
    'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d': 'eyJpdiI6InhNS3NxVmZBYnhCSG5hSzN3TkNGYnc9PSIsInZhbHVlIjoiOUgza0U2UDZMakNwOUhXWGh3VmovVUNEQUFLYUZmcldHQUs4WUNKdzZYUVhvWE5sT08xUERzRE9MZWt0MlRaLzRMUk4wT01Zcy9WQ3FQZ0EyS0hCclpZOHdLUWtVVm1mMFpJZFBmTUJPNnIwcFBVT3JuT2lNMHRHM2dBM3B0SDhQQW5XS1Z2YXJEbjdiK1VKMS90U0hrZjNpcE9qT2JOdTJKWjRGaXN0dzgwN2VTbmVlbGNmTkZvSkMvbFVQVjZqTkgvckdkN2FrL2tzRTNVdVdVSUZOYno5VVBaS0E4emV1eUt3ZlV1WExaZz0iLCJtYWMiOiJhODI3OTZkM2YwOTI3NWVkYWNiMjYyMzY0MDY3ZjJhYzM3NDQ4NzA3ZDk0MjdlMDBlMDI4NTIzYWZlMDg5MTM0IiwidGFnIjoiIn0%3D',
    'XSRF-TOKEN': 'eyJpdiI6Ikx2WnBRd1VLYjRHaUd2dXBWcklmTkE9PSIsInZhbHVlIjoiM1ZiNWdtbkhrTzZpaE9iV2RtUHV1T05vdXNIWGRxSjI5RW4yblhaM0ttZGgrQUtMcVIra1dRZmhuQnRqRzlNVEp5Q1JWajVycjZWM1VjM1cxMmhjYndobTN4RjdtNjhSU3pZb0cxOThPeFNMN0N4WVNnbG55MjJaNkRpTWtPYjAiLCJtYWMiOiI4ZmJhMDVkN2E5MzljNmZkNDFhZjA0MjNmYTMxYWYwMTczYjNmNjU4NDlhN2U3NmMwYjEzMzZhNjFhYTFmMjg5IiwidGFnIjoiIn0%3D',
    'laravel_session': 'eyJpdiI6Im5mZVZvaGVpZHlENHp3RmYzQkRoWnc9PSIsInZhbHVlIjoiQ25RbDdMR0F4MTZrbEEzTld3ZHVtcVNNcHRNQWFHdDZsOThpRUwvcnpIb1FQQVVKWG1CZ0ZsM1dUQ0RIWjRtMmpKeE5VZDFjMDdjcVBaRGlkcWFkY29vOHBhZzducjc2S2ZMdC9MN3lpZjdta1BLaHgwVG0yYXBwdUNGZDFIMEIiLCJtYWMiOiI1YmJkOTA0NWEyZDk3ZTY2NzZhZWVkZjgwMzFmNzU5YmI3NTk1ZjBhNjVlZWIyZDZlZmQxNzc2ODBjNjRhZTYyIiwidGFnIjoiIn0%3D',
}

headers = {
    'authority': 'www.ge-tracker.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'ips4_IPSSessionFront=1mdjcf2rvhdoc0upmhvjkcm0l4; __stripe_mid=c87e7271-a75f-44b8-9568-dcd3a134c6e44fc640; cf_clearance=8Id6Si0fCx2aj.eUyKTa.IoGZpPVFOVFqoPY1iH.D5g-1656182299-0-150; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6InhNS3NxVmZBYnhCSG5hSzN3TkNGYnc9PSIsInZhbHVlIjoiOUgza0U2UDZMakNwOUhXWGh3VmovVUNEQUFLYUZmcldHQUs4WUNKdzZYUVhvWE5sT08xUERzRE9MZWt0MlRaLzRMUk4wT01Zcy9WQ3FQZ0EyS0hCclpZOHdLUWtVVm1mMFpJZFBmTUJPNnIwcFBVT3JuT2lNMHRHM2dBM3B0SDhQQW5XS1Z2YXJEbjdiK1VKMS90U0hrZjNpcE9qT2JOdTJKWjRGaXN0dzgwN2VTbmVlbGNmTkZvSkMvbFVQVjZqTkgvckdkN2FrL2tzRTNVdVdVSUZOYno5VVBaS0E4emV1eUt3ZlV1WExaZz0iLCJtYWMiOiJhODI3OTZkM2YwOTI3NWVkYWNiMjYyMzY0MDY3ZjJhYzM3NDQ4NzA3ZDk0MjdlMDBlMDI4NTIzYWZlMDg5MTM0IiwidGFnIjoiIn0%3D; XSRF-TOKEN=eyJpdiI6Ikx2WnBRd1VLYjRHaUd2dXBWcklmTkE9PSIsInZhbHVlIjoiM1ZiNWdtbkhrTzZpaE9iV2RtUHV1T05vdXNIWGRxSjI5RW4yblhaM0ttZGgrQUtMcVIra1dRZmhuQnRqRzlNVEp5Q1JWajVycjZWM1VjM1cxMmhjYndobTN4RjdtNjhSU3pZb0cxOThPeFNMN0N4WVNnbG55MjJaNkRpTWtPYjAiLCJtYWMiOiI4ZmJhMDVkN2E5MzljNmZkNDFhZjA0MjNmYTMxYWYwMTczYjNmNjU4NDlhN2U3NmMwYjEzMzZhNjFhYTFmMjg5IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6Im5mZVZvaGVpZHlENHp3RmYzQkRoWnc9PSIsInZhbHVlIjoiQ25RbDdMR0F4MTZrbEEzTld3ZHVtcVNNcHRNQWFHdDZsOThpRUwvcnpIb1FQQVVKWG1CZ0ZsM1dUQ0RIWjRtMmpKeE5VZDFjMDdjcVBaRGlkcWFkY29vOHBhZzducjc2S2ZMdC9MN3lpZjdta1BLaHgwVG0yYXBwdUNGZDFIMEIiLCJtYWMiOiI1YmJkOTA0NWEyZDk3ZTY2NzZhZWVkZjgwMzFmNzU5YmI3NTk1ZjBhNjVlZWIyZDZlZmQxNzc2ODBjNjRhZTYyIiwidGFnIjoiIn0%3D',
    'referer': 'https://www.ge-tracker.com/item/old-school-bond',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}

response = requests.get('https://www.ge-tracker.com/auth/login', cookies=cookies, headers=headers)

soup1 = BeautifulSoup(response.content, 'html.parser')
#print(soup1)

scraper = cfscrape.create_scraper() #Bypasses cloudfare by utilizing nodejs
res = scraper.get("https://www.ge-tracker.com/item/old-school-bond").text #Scrapes data from ge-tracker
#print(res)

soup = BeautifulSoup(res, 'html.parser') #parses res.text as html
results = soup # changes soup to results for easier recall
#print(results)

buy=results.find_all(id="v_item_page") #Finds all data between <div id="v_item_page"> and </div>]
#print(buy) #Prints all data from line above
buy2 = str(buy) # Turns data into string for manipulation
#print(buy2) # Shows data

def allNumbers(string):            # Creates all number string function
    regex = re.compile(r'\d+')     # Hard to tell
    return regex.findall(string)   # Hard to tell

buydata = (allNumbers(buy2)) #Assigns all numbers to a variable allowing for easier manipulation of data later

#print(buydata) #Displays (allNumbers(buy2)) or simply displays all numbers found for data manipulation

import numpy as np
buyarray1=np.array(buydata)
#print(buyarray1)

buySellRatio=buyarray1[15]
print(buySellRatio)
buySellRatio2=buyarray1[16]
print(buySellRatio2)

if sum(c.isdigit() for c in buySellRatio2) == 2:
    buySellRatioActual = int(buySellRatio)+(int(buySellRatio2)/100)
    print(buySellRatioActual)
    if sum(c.isdigit() for c in buySellRatio2) == 1:
        buySellRatioActual = int(buySellRatio) + (int(buySellRatio2) / 10)
        print(buySellRatioActual)
        if sum(c.isdigit() for c in buySellRatio) >= 3:
            a1 = (a+1)
            b1 = (b+1)
            c1 = (c+1)
            d1 = (d+1)
            e1 = (e+1)
            f1 = (f+1)
            g1 = (g+1)
