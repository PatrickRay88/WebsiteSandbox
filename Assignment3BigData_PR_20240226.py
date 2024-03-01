# -*- coding: utf-8 -*-
"""
Date: 02/25/2024
Description: Python script to pull data from API, load into REDIS database and then extract and commpute
API from rentcast.io 
https://redis.io/docs/connect/clients/python/
https://www.dragonflydb.io/code-examples/getting-json-values-from-redis-in-python
"""

import requests
from db_config import get_redis_connection
import matplotlib.pyplot as plt
import numpy as np
key = "somekey"
###################################
#      API from rentcast.io       #
###################################

class API:    
   def API_call():
       '''
       
       Returns
       -------
       dataDict = JSONData.json()
        Pulls JSON data from an API call in the variable.
       '''
       
       url = "https://api.rentcast.io/v1/avm/value?address=5500%20Grand%20Lake%20Drive%2C%20San%20Antonio%2C%20TX%2C%2078244&propertyType=Single%20Family&bedrooms=4&bathrooms=2&squareFootage=1600&compCount=20"
       headers = {
            "accept": "application/json",
            "X-Api-Key": "53103c8e74074e6e868895e2b8395868"
            }
       JSONData = requests.get(url, headers=headers)
       if JSONData.status_code == 200:
            # Return the JSON data_dict
         return JSONData.json()

###############################
#       REDIS Handling        #
###############################

class Redis:
    def upLoadData(dataDict):
        '''
        

        Parameters
        ----------
        dataDict : Python Data Dictionary
            Data retrieved from API class.
        key : string 
            Sets the key for uploading JSON data
        Returns
        -------
        None. Uploads JSON file to Redis database

        '''
        r.json().set("somekey", ".", dataDict)

    def retreiveData(key):
        '''
        
        
        Parameters
        ----------
        key : String
            Sets the key for uploading JSON data
        Returns
        -------
        days_old_list, prices : data list

        '''
    #extracting from redis db 
        data = r.json().get(key)
        prices = [data['price']] + [comp['price'] for comp in data['comparables']]
        days_old_list = [comp['daysOld'] for comp in data['comparables']]
    #Formating the data if necc. and error checking 
        if len(prices)>len(days_old_list):
            prices = prices[1:]    
        if prices is not None and days_old_list is not None: 
            print("Retrieve data successfull")
        else:
            print("data extraction failed")
        return days_old_list, prices

#############################################################
## Use API / Load / Extract REDIS Data and do some ploting ##
#############################################################
if __name__ == "__main__":
    
    #establish connection
    r = get_redis_connection()
    
    #Load/ extract and Plot data
    dataDict = API.API_call()
    Redis.upLoadData(dataDict)
    days_old_list, prices = Redis.retreiveData(key)
    
    '''
    Plot the prices against the amount of days old
    and then,
    Plot a trendline
    
    '''
    #set up subplots
    fig, axs = plt.subplots(2, 1, figsize=(8, 10))
    
    axs[0].plot(prices, days_old_list, 'o', label='Data')
    axs[0].set_xlabel('Price')
    axs[0].set_ylabel('Days Old')
    axs[0].set_title('Price vs Days Old')
    axs[0].legend()
    
    #do some maths
    coefficients = np.polyfit(prices, days_old_list, 1)
    polynomial = np.poly1d(coefficients)
    
    axs[1].plot(prices, days_old_list, 'o', label='Data')
    axs[1].set_xlabel('Price')
    axs[1].set_ylabel('Days Old')
    axs[1].plot(prices, polynomial(prices), color='red',label='Trendline')
    axs[1].set_xlabel('Price')
    axs[1].set_ylabel('Days Old')
    axs[1].set_title('Price vs Days Old')
    axs[1].legend()
    plt.show()