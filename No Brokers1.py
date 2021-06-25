#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install bs4')
get_ipython().system('pip install requests')
get_ipython().system('pip install html5lib')


# In[5]:


from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time


# In[3]:


Page =requests.get("https://www.nobroker.in/property/sale/bangalore/Electronic%20City?type=BHK4&searchParam=W3sibGF0IjoxMi44NDUyMTQ1LCJsb24iOjc3LjY2MDE2OTUsInBsYWNlSWQiOiJDaElKdy1GUWQ0cHNyanNSSGZkYXpnXzhYRW8iLCJwbGFjZU5hbWUiOiJFbGVjdHJvbmljIENpdHkifV0=&propertyAge=0&radius=2.0%22")
Page


# In[4]:


soup=BeautifulSoup(Page.content)
soup


# In[ ]:


timestr = time.strftime("%Y%m%d-%H%M%S")

# Creating empty list
Title = []
Area = []
Location = []
Emi= []
Price = []

def scrape_NoBroker(n):
    print(f'Exporting {n} rows!!!')

    try:
        for page in range(int(n / 10)):

            try:
                print(f'{(page + 1) * 10} rows added!!!')

                # Requesting URL
                url = requests.get(
                    'https://https://www.nobroker.in/property/sale/bangalore/Electronic%20City?type=BHK4&searchParam=W3sibGF0IjoxMi44NDUyMTQ1LCJsb24iOjc3LjY2MDE2OTUsInBsYWNlSWQiOiJDaElKdy1GUWQ0cHNyanNSSGZkYXpnXzhYRW8iLCJwbGFjZU5hbWUiOiJFbGVjdHJvbmljIENpdHkifV0=&propertyAge=0&radius=2.0%22' + str(
                        page)).text

                # Converting from HTML tag to BeautifulSoup object
                soup = BeautifulSoup(url, 'lxml')

                # Finding all the div tag wich contains all the info
                houses = soup.find_all('div', class_='card')

                # Looping through each div tag to get individual content
                for house in houses:
                    title.append(house.find('a', class_='card-link-detail')['title'][:1])
                    Area_raw = house.find('a', class_='card-link-detail')['title']
                    if ',' in Area_raw:
                        Area.append(Area_raw.split(',')[-1])
                    else:
                        Area.append(Area_raw.split('in', 1)[-1])
                    Location.append(house.find('meta', itemprop='latitude')['content'])
                    Emi.append(house.find_all('meta', itemprop='value')[0]['content'])
                    Price.append(house.find_all('meta', itemprop='value')[1]['content'])
                    
            except:
                print(f'Row number {(page + 1) * 10} failed. Trying next one!!!')
    except:
        pass

    df = pd.DataFrame(list(zip(Title, Area, Location, Emi, Price)),
                      columns=['Title', 'Area', 'Location', 'Emi', 'Price(Rs)'])

   
    File_name = "House_Data_" + timestr + ".csv"
    df.to_csv(File_name, index=False)
    print("File Exported Sucessfully!!!!")


scrape_NoBroker(100)


# In[ ]:




