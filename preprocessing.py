from cleaning import Cleaning
import pandas as pd

class Preprocessing:
    def group_by_hour_by_day(self, crash):
        """It group row by hour by day to see how many accident, injured and killed"""

        """First we combine day (changed to day name) and time column and drop column not needed"""
        crash['crash_date'] = pd.to_datetime(crash['crash_date'], format='%Y-%m-%d')
        crash['crash_date'] = crash['crash_date'].dt.day_name()
        crash['crash_time'] = pd.to_datetime(crash['crash_time'], format='%H:%M').dt.hour
        crash['crash_date'] = crash['crash_date'].astype(str) +" "+ crash['crash_time'].astype(str)
        crash.drop(['crash_time', 'borough', 'zip_code', 'latitude', 
                    'longitude', 'location', 'on_street_name', 'off_street_name',
                    'cross_street_name', 'contributing_factor_vehicle_1', 'contributing_factor_vehicle_2',
                    'contributing_factor_vehicle_3', 'contributing_factor_vehicle_4', 'contributing_factor_vehicle_5',
                    'collision_id', 'vehicle_type_code1', 'vehicle_type_code2', 'vehicle_type_code_3', 
                    'vehicle_type_code_4', 'vehicle_type_code_5'], axis = 1, inplace = True)
        
        """We are groupping by crash time to see when we had the most injuried and killed"""

        crash = crash.groupby(crash['crash_date']).mean()

        return crash

crash = Cleaning().import_csv('final.csv')
crash = Preprocessing().group_by_hour_by_day(crash)

print(crash)
print(crash.describe())