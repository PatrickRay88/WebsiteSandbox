# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 08:51:57 2024

@author: patri
"""
import pandas as pd
import aiohttp
import asyncio
from geopy.geocoders import Nominatim

# async def fetch_geocode(session, town):
#     url = f"https://nominatim.openstreetmap.org/search?q={town}&format=json&limit=1"
#     async with session.get(url) as response:
#         data = await response.json()
#         if data:
#             return town, data[0]['lat'], data[0]['lon']
#         else:
#             return town, None, None
async def fetch_geocode(session, town):
    url = f"https://nominatim.openstreetmap.org/search?q={town}&format=json&limit=1"
    async with session.get(url) as response:
        if response.content_type == 'application/json':
            data = await response.json()
            if data:
                return town, data[0]['lat'], data[0]['lon']
            else:
                return town, None, None
        else:
            print(f"Unexpected content type: {response.content_type}")
            return town, None, None
async def process_batch(session, batch):
    tasks = [fetch_geocode(session, town) for town in batch]
    return await asyncio.gather(*tasks)

async def main():
    file_path = 'C:\\Users\\patri\\OneDrive\\Desktop\\Real_Estate_Sales_2001-2021.csv'
    data = pd.read_csv(file_path, low_memory=False)
    towns = data['Town'].unique()
    
    geolocator = Nominatim(user_agent="town_geocoder")
    batch_size = 100  # Adjust batch size as needed
    
    async with aiohttp.ClientSession() as session:
        results = []
        for i in range(0, len(towns), batch_size):
            batch = towns[i:i+batch_size]
            results.extend(await process_batch(session, batch))
    
    results_df = pd.DataFrame(results, columns=['Town', 'Latitude', 'Longitude'])
    merged_data = pd.merge(data, results_df, on='Town', how='left')
    
    updated_file_path = 'C:\\Users\\patri\\OneDrive\\Desktop\\Real_Estate_Sales_2001-2021wLATLONG.csv'
    merged_data.to_csv(updated_file_path, index=False)
    print("Latitude and longitude coordinates added successfully.")

asyncio.create_task(main())

# import pandas as pd
# import aiohttp
# import asyncio
# from geopy.geocoders import Nominatim

# async def fetch_geocode(session, town):
#     url = f"https://nominatim.openstreetmap.org/search?q={town}&format=json&limit=1"
#     async with session.get(url) as response:
#         data = await response.json()
#         if data:
#             return town, data[0]['lat'], data[0]['lon']
#         else:
#             return town, None, None

# async def process_batch(session, batch):
#     tasks = [fetch_geocode(session, town) for town in batch]
#     return await asyncio.gather(*tasks)

# async def main():
#     file_path = 'C:\\Users\\patri\\OneDrive\\Desktop\\Real_Estate_Sales_2001-2021 - Copy.csv'
#     data = pd.read_csv(file_path, low_memory=False)
#     towns = data['Town'].unique()
    
#     geolocator = Nominatim(user_agent="town_geocoder")
#     batch_size = 100  # Adjust batch size as needed
    
#     async with aiohttp.ClientSession() as session:
#         results = []
#         for i in range(0, len(towns), batch_size):
#             batch = towns[i:i+batch_size]
#             results.extend(await process_batch(session, batch))
    
#     results_df = pd.DataFrame(results, columns=['Town', 'Latitude', 'Longitude'])
#     merged_data = pd.merge(data, results_df, on='Town', how='left')
    
#     updated_file_path = 'C:\\Users\\patri\\OneDrive\\Desktop\\Real_Estate_Sales_2001-2021wLATLONG.csv'
#     merged_data.to_csv(updated_file_path, index=False)
#     print("Latitude and longitude coordinates added successfully.")

# if __name__ == "__main__":
#     asyncio.run(main())

# import pandas as pd
# from geopy.geocoders import Nominatim
# from multiprocessing import Pool

# file_path = 'C:\\Users\\patri\\OneDrive\\Desktop\\Real_Estate_Sales_2001-2021 - Copy.csv'
# data = pd.read_csv(file_path, low_memory=False)

# # Initialize geocoder
# geolocator = Nominatim(user_agent="town_geocoder")

# # Function to get latitude and longitude for a town name
# def get_lat_lon(town):
#     location = geolocator.geocode(town)
#     if location:
#         return town, location.latitude, location.longitude
#     else:
#         return town, None, None

# # Convert DataFrame to list of dictionaries
# data_list = data.to_dict('records')

# # Define a function to process each row
# def process_row(row):
#     town = row['Town']
#     return get_lat_lon(town)

# # Use multiprocessing Pool to parallelize the geocoding process
# with Pool() as pool:
#     results = pool.map(process_row, data_list)

# # Convert results back to DataFrame
# results_df = pd.DataFrame(results, columns=['Town', 'Latitude', 'Longitude'])

# # Merge results DataFrame with original DataFrame on 'Town'
# data_merged = pd.merge(data, results_df, on='Town', how='left')

# # Save the updated dataset to a new CSV file
# updated_file_path = 'C:\\Users\\patri\\OneDrive\\Desktop\\Real_Estate_Sales_2001-2021wLATLONG.csv'
# data_merged.to_csv(updated_file_path, index=False)

# print("Latitude and longitude coordinates added successfully.")

# import pandas as pd
# from geopy.geocoders import Nominatim
# from multiprocessing import Pool

# file_path = 'C:\\Users\\patri\\OneDrive\\Desktop\\Real_Estate_Sales_2001-2021 - Copy.csv'
# data = pd.read_csv(file_path, low_memory=False)

# # Initialize geocoder
# geolocator = Nominatim(user_agent="town_geocoder")

# # Function to get latitude and longitude for a town name
# def get_lat_lon(town):
#     location = geolocator.geocode(town)
#     if location:
#         return town, location.latitude, location.longitude
#     else:
#         return town, None, None

# # Define a function to process each row
# def process_row(row):
#     town = row['Town']
#     return get_lat_lon(town)

# # Use multiprocessing Pool to parallelize the geocoding process
# with Pool() as pool:
#     results = pool.map(process_row, data.itertuples(index=False))

# # Update the dataframe with latitude and longitude
# for result in results:
#     town, latitude, longitude = result
#     idx = data.index[data['Town'] == town].tolist()[0]
#     data.at[idx, 'Latitude'] = latitude
#     data.at[idx, 'Longitude'] = longitude

# # Save the updated dataset to a new CSV file
# updated_file_path = 'C:\\Users\\patri\\OneDrive\\Desktop\\Real_Estate_Sales_2001-2021wLATLONG.csv'
# data.to_csv(updated_file_path, index=False)

# print("Latitude and longitude coordinates added successfully.")


# Load your dataset CSV file
# file_path = 'C:\\Users\\patri\\OneDrive\\Desktop\\Real_Estate_Sales_2001-2021 - Copy.csv'
# data = pd.read_csv(file_path, low_memory=False)

# # Initialize geocoder
# geolocator = Nominatim(user_agent="town_geocoder")

# # Function to get latitude and longitude for a town name
# def get_lat_lon(town):
#     location = geolocator.geocode(town)
#     if location:
#         return location.latitude, location.longitude
#     else:
#         return None, None

# # Add latitude and longitude columns to the dataset
# data['Latitude'] = None
# data['Longitude'] = None

# # Iterate over each row and geocode town names
# for index, row in data.iterrows():
#     town = row['Town']
#     latitude, longitude = get_lat_lon(town)
#     data.at[index, 'Latitude'] = latitude
#     data.at[index, 'Longitude'] = longitude

# # Save the updated dataset to a new CSV file
# updated_file_path = 'C:\\Users\\patri\\OneDrive\\Desktop\\Real_Estate_Sales_2001-2021wLATLONG.csv'
# data.to_csv(updated_file_path, index=False)

# print("Latitude and longitude coordinates added successfully.")