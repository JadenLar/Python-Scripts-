import requests
from bs4 import BeautifulSoup
import cfscrape
import re

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


# Rows 62 - 155 Represent the data as an array and assign rows in that array to variables completing data setup
import numpy as np
buyarray1 =np.array(buydata)
#print(buyarray1)

day_price=buyarray1[0]
print(day_price)

day_volume=buyarray1[1]
print(day_volume)

month3_price=buyarray1[3]
print(month3_price)

month6_price=buyarray1[5]
print(month6_price)

month_price=buyarray1[6]
print(month_price)

week_price=buyarray1[7]
print(week_price)

year_price=buyarray1[8]
print(year_price)

initialItem=buyarray1[9]
print(initialItem)

itemId=buyarray1[10]
print(itemId)

buyingQuantity=buyarray1[13]
print(buyingQuantity)

sellingQuantity=buyarray1[14]
print(sellingQuantity)

buySellRatio=buyarray1[15]
#print(buySellRatio)

buySellRatio2=buyarray1[16]

a1 = 17
b1 = 18
c1 = 19
d1 = 20
e1 = 21
f1 = 34
g1 = 35
h1 = 36

if sum(c.isdigit() for c in buySellRatio2) == 2:
    buySellRatioActual = int(buySellRatio)+(int(buySellRatio2)/100)
    print(buySellRatioActual)
    if sum(c.isdigit() for c in buySellRatio2) == 1:
        buySellRatioActual = int(buySellRatio) + (int(buySellRatio2) / 10)
        print(buySellRatioActual)
        if sum(c.isdigit() for c in buySellRatio) >= 3:
            a1 = (a1-1)
            b1 = (b1-1)
            c1 = (c1-1)
            d1 = (d1-1)
            e1 = (e1-1)
            f1 = (f1-1)
            g1 = (g1-1)
            h1 = (h1-1)
        else:
            buySellRatio2 == "no decimal"
            print("no decimal")

overall=buyarray1[a1]
print(overall)

buying=buyarray1[b1]
print(buying)

selling=buyarray1[c1]
print(selling)

approxProfit=buyarray1[d1]
print(approxProfit)

tax=buyarray1[e1]
print(tax)

buyLimit=buyarray1[f1]
print(buyLimit)

lowAlch=buyarray1[g1]
print(lowAlch)

highAlch=buyarray1[h1]
print(highAlch)

#overall is mean price over last 5 minutes
#day_price is the mean price over the total day
#so if the overall is 90-110% of the overall then
# so if the current 5 minute overall is deviated by more than 10% negatively then we auto place an order at the lowest
# price avaiable, given that price is actually within the price range we are willing to act on (-10% at minimum)


# Determining % Difference in current price and overall price
print()
print("------line break------")
print("------line break------")
print("------line break------")
print()

print("Price of the day:", day_price)
print("5 Minute price:", overall)
if (int(day_price) - (int(overall))) > (int(day_price)*.04):
    print("Profitable margin!")
    Volatil = (int(overall) - int(day_price))
    print("Difference in price in GP:", Volatil)
else:
    print("If you see this it means the Current price is within greater than 96% of the day price")
    Volatil = (int(overall) - int(day_price))
    print("Difference in price in GP:", Volatil)

VolatilPercent = 100 * (int(overall) - int(day_price)) / int(day_price)
print("Margin% =", VolatilPercent,"%")

