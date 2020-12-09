import pandas as pd
import numpy as np
import re

from geopy.geocoders import Nominatim

class Cleaning:
    """With this class i will start to clean. I will delete row with a lot of NaN value
    or just change NaN by something else (depending on columns)"""

    def import_csv(self, csv_file: str):
        """We just import csv file as DataFrame and return a DataFrame"""
        crash = pd.read_csv(csv_file)
        print(crash.head())
        return crash

    def change_type(self, crash):
        """It changes the type object to something else (like date time, or str)"""

        crash['crash_date'] = pd.to_datetime(crash['crash_date'], format='%Y-%m-%d')
        crash['zip_code'] = crash['zip_code'].fillna(0)
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
                crash[name] = crash[name].fillna('unkown')
            else:
                crash[name] = crash[name].fillna(0)
        return crash
        
    def delete_duplicated(self, crash):
        """Will drop cuplicated row"""
        crash = crash.drop_duplicates()
        return crash

    def finding_missing_value(self, crash):
        """With reverse geocoding, it will find missing value"""
        g = Nominatim(user_agent="nyc-crashes")
        location = g.reverse((crash['latitude'][0], crash['longitude'][0]))
        print(location)
        for i in crash.index: #à corriger
            print(crash['zip_code'][i])
            if crash['zip_code'][i].isnull():
                if crash['latitude'][i].isnull():
                    location = g.reverse((crash['latitude'][i], crash['longitude'][i]))
                    crash['zip_code'][i] = (location.raw['address']['postcode'])
        return crash

crash = Cleaning().import_csv("data_test.csv")
crash = Cleaning().finding_missing_value(crash)
print(crash.isnull().sum())
#crash = Cleaning().change_type(crash)
#crash = Cleaning().cleaning_space(crash)
#crash = Cleaning().replace_NaN_value(crash)
#crash = Cleaning().delete_duplicated(crash)

#g = Nominatim(user_agent="nyc-crashes")
#location = g.reverse((40.602757, -73.96377))
#print(location.raw)