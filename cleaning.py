import pandas as pd
import numpy as np
import re

from geopy.geocoders import Nominatim

from multiprocessing import Pool

class Cleaning:
    """With this class i will start to clean. I will delete row with a lot of NaN value
    or just change NaN by something else (depending on columns)"""

    def import_csv(self, csv_file: str):
        """We just import csv file as DataFrame and return a DataFrame"""
        crash = pd.read_csv(csv_file)
        return crash

    def change_type(self, crash):
        """It changes the type object to something else (like date time, or str)"""

        crash['crash_date'] = pd.to_datetime(crash['crash_date'], format='%Y-%m-%d')
        crash['zip_code'] = crash['zip_code'].astype(int)
        

        return crash

    def cleaning_space(self, crash):
        """Will delete unnecessary space"""

        for name in crash.columns:
            if crash[name].dtype == object :
                crash[name] = crash[name].replace(r'\s+', ' ', regex=True)
                crash[name] = crash[name].str.strip()
        return crash
    
    def replace_NaN_value(self, crash):
        """Will replace NaN value depending of type of the value, knowing that zip_code already replace by 0"""

        for name in crash.columns:
            if crash[name].dtype == object:
                crash[name] = crash[name].fillna('Unspecified')
            else:
                crash[name] = crash[name].fillna(-1)
        return crash
        
    def delete_duplicated(self, crash):
        """Will drop cuplicated row"""
        crash = crash.drop_duplicates()
        return crash
    
    def check_value_long_lat_and_change(self, crash):
        """It will check if value of lat and long is out of limit"""

        crash.loc[crash['latitude'] > 90, 'latitude'] = -1
        crash.loc[crash['latitude'] < -90, 'latitude'] = -1
        crash.loc[crash['longitude'] > 180, 'longitude'] = -1
        crash.loc[crash['longitude'] < -180, 'longitude'] = -1
        crash['latitude'] = crash['latitude'].fillna(-1)
        crash['longitude'] = crash['longitude'].fillna(-1)
        
        return crash

    def finding_missing_value(self, crash):
        """With reverse geocoding, it will find missing value
        Since this function too much time i won't use it"""
           
        g = Nominatim(user_agent="nyc-crashes")
        idx = crash['zip_code'].index[crash['zip_code'].apply(np.isnan)]
        for i in idx:
            if crash['longitude'][i] != -1 and crash['latitude'][i] != -1:
                location = g.reverse((crash['latitude'][i], crash['longitude'][i]))
                if location.raw['address'] != np.nan and 'postcode' in location.raw['address']:
                    crash['zip_code'][i] = location.raw['address']['postcode']
            if i > 1000:
                print(i)
        
        return crash


    def apply_parallel(self, df, func):
        """function which will run a multiprocessing pool"""
        n_cores = 4
        pool = Pool(n_cores)
        # split dataframe
        df_split = np.array_split(df, n_cores)
        # calculate metrics for each and concatenate
        df = pd.concat(pool.map(func, df_split))
        return df
 
    def all_function(self, file: str):
        """For importing all function at once"""

        crash = Cleaning().import_csv(file)
        #crash = Cleaning().finding_missing_value(crash)
        crash = Cleaning().replace_NaN_value(crash)
        crash = Cleaning().check_value_long_lat_and_change(crash)
        crash = Cleaning().change_type(crash)
        crash = Cleaning().cleaning_space(crash)
        return crash

    def create_final_csv(self, crash):
        """This function is used to create a cleanded csv file"""

        crash.to_csv('final.csv', index=False)
