
# coding: utf-8

# # WeatherPy Analysis 
# 

# ### Analysis 
# 
# ### Based on the data the temperature of the cities increases as they get closer to the equator. 
# 
# ### Another observation is that althogh the coordinates of the cities are selected ramdonly, there exist some bias due to the proximity of the cities. 
# 
# ### In addition, there are some cities that do not follow the assumption that cities next to the eqautor will always have a tropical weather. This obsevation can be determined  from the analysis on humidity and cloudiness. 

# In[19]:


#Importing dependecies 
import time
import pandas as pd
import numpy as np
import requests as req
import json
import matplotlib.pyplot as plt 
import openweathermapy.core as owm
from config import api_key
import seaborn as sns 
from citipy import citipy


# In[2]:


# Open Weathermap API Key 
owkey = "f20c07a3cdc97c14e48c7167d623898b"
# Google Maps API Key 
# gkey = "AIzaSyDAVk_JHRsVV8rnyvELr0llXo9ORVGcTwM"
# print (gkey)


# In[3]:


#build a dataframe to hold lat and log values
locations_df = pd.DataFrame()

# create var to hold the random lat and log values 

locations_df['rand_lat'] = [np.random.uniform(-90,90) for x in range(1500)]
locations_df['rand_lng'] = [np.random.uniform(-180, 180) for x in range(1500)]

locations_df.tail()


# In[4]:


# add closest city and country column
locations_df['closest_city'] = ""
locations_df['country'] = ""

#find and add closest city and country code
for index, row in locations_df.iterrows():
    lat = row['rand_lat']
    lng = row['rand_lng']
    locations_df.set_value(index, 'closest_city', citipy.nearest_city(lat, lng).city_name)
    locations_df.set_value(index, 'country', citipy.nearest_city(lat, lng).country_code)


# In[5]:


# delete repeated cities and find unique city count
locations_df = locations_df.drop_duplicates(['closest_city', 'country'])
locations_df = locations_df.dropna()
len(locations_df['closest_city'].value_counts())


# In[6]:


#preview data
locations_df.tail()


# In[7]:


#cleaning and formating the columns 
locations_df = locations_df.rename(columns = {'closest_city': 'city'})
locations_df=locations_df[['city', 'country']]
locations_df.head()


# In[8]:


#create columns for Latitude, Longitud ,Humitity , Wind Speed, Cloudiness

locations_df['Cloudiness (%)'] = ""
locations_df['Humidity (%)'] = ""
locations_df['Wind Speed (mph)'] = ""
locations_df['Temperature (F)']= ""
locations_df['Latitude']= ""
locations_df['Longitude']= ""
locations_df.tail()


# In[9]:


# Accessing data
print("Beginning Data Retrieval")
print("---------------------------------")

# # Limiting pull requests
# start_time = time.time()

for index, row in locations_df.iterrows():
   # Building target url
   url = "http://api.openweathermap.org/data/2.5/weather?q=%s,%s&units=imperial&appid=%s" % (row['city'],
                                                                                             row['country'], owkey)
   # Printing to ensure loop is correct
   print("Now retrieving City #" + str(index) + ": " + row['city'] + ", " + row['country'])
   print(url)
   
   # Running request
   weather_data = req.get(url).json()

   
   try:
       # Appending latitude and longitude to correct location
       row['Latitude'] = weather_data['coord']['lat']
       row['Longitude'] = weather_data['coord']['lon']
   
       # Appending temperature to correct location
       row['Temperature (F)'] = weather_data['main']['temp']
   
       # Appending humidity to correct location
       row['Humidity (%)'] = weather_data['main']['humidity']
   
       # Appending cloudiness to correct location
       row['Cloudiness (%)'] = weather_data['clouds']['all']
   
       # Appending wind speed to correct location
       row['Wind Speed (mph)'] = weather_data['wind']['speed']
   except:
       print("Error with city data. Skipping")
       continue
       
# #    Pausing to limit pull requests
#    if (index + 1) % 60 == 0:
#        run_time = time.time() - start_time
#        time.sleep(60 - run_time)
    
   
print("---------------------------------")
print("Data Retrieval Complete")
print("---------------------------------")






# In[14]:


# locations_df.dropna(axis = 0, how = 'any',thresh=None, subset=None, inplace= False)
# locations_df.dropna()

# locations_df.dropna(axis="rows", how = 'any')

locations_df['Cloudiness (%)'].replace('', np.nan, inplace=True)
locations_df.dropna(axis = 0, how = 'any',thresh=None, subset=None, inplace= True)
locations_df


# In[42]:


Lat = locations_df["Latitude"]
Temp = locations_df['Temperature (F)']
hum= locations_df['Humidity (%)']
cloud = locations_df['Cloudiness (%)']
wind = locations_df['Wind Speed (mph)']




# In[36]:


#Temperature (F) vs. Latitude



plt.title("Temperature vs Latitude")
plt.axvline(0, color = 'black', alpha = .25, label = 'Equator')
plt.xlabel('Latitude')
plt.ylabel('Temperature (F)')
plt.ylim(-5,105)
plt.text(1,30,'Equator',rotation=90)
plt.scatter(Lat, Temp)
plt.show()
plt.savefig("Temperature vs Latitude")


# In[37]:


#Humidity (%) vs. Latitude
plt.title("Humidity (%) vs Latitude")
plt.xlabel('Latitude')
plt.ylabel('Humidity (%)')
plt.ylim(-5,105)
plt.axvline(0, color = 'black', alpha = .25, label = 'Equator')
plt.text(1,30,'Equator',rotation=90)
plt.scatter(Lat, hum)
plt.show()
plt.savefig("Humidity (%) vs Latitude")


# In[38]:


#Cloudiness (%) vs. Latitude
plt.title('Cloudiness (%) vs Latitude')
plt.xlabel('Latitude')
plt.ylabel('Cloudiness (%)')
plt.ylim(-5,105)
plt.axvline(0, color = 'black', alpha = .25)
plt.text(1,30,'Equator',rotation=90)
plt.scatter(Lat, cloud)
plt.show()
plt.savefig('Cloudiness (%) vs Latitude')


# In[41]:


#Wind Speed (mph) vs. Latitude

plt.title('Wind Speed (mph) vs Latitude')
plt.xlabel('Latitude')
plt.ylabel('Wind Speed (mph)')
plt.ylim(-5,105)
plt.axvline(0, color = 'black', alpha = .25)
plt.text(1,30,'Equator',rotation=90)
plt.scatter(Lat, wind)
plt.show('Wind Speed (mph) vs Latitude')
plt.savefig('Wind Speed (mph) vs Latitude')

