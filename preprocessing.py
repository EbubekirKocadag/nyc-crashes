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
        
        """We are groupping by crash time to see when we had the most injuried and killed
        and add new column to be able to now how many accident we had"""

        crash['quantity'] = 1
        quantity = crash['quantity'].groupby(crash['crash_date']).sum()
        crash = crash.groupby(crash['crash_date']).mean()
        crash['quantity'] = quantity

        return crash

    def group_data_give_quantity(self, groupby_value: str, wanted_list: list, crash):
        """General function which with given column that we want to group with the list of column name that
        we want to take mean value. It will give quantity of grouped value too"""

        columns = list(crash.columns)
        wanted_list.append(groupby_value)
        final_list = []

        for i in columns:
            if i not in wanted_list:
                final_list.append(i)
        crash.drop(final_list, axis= 1, inplace= True)

        """We will group by groupby and add quantity column"""
        crash['quantity'] = 1
        quantity = crash['quantity'].groupby(crash[groupby_value]).sum()
        crash = crash.groupby(crash[groupby_value]).mean()
        crash['quantity'] = quantity
        
        return crash

    #def nominalizatio_of_function(self,)
        

crash = Cleaning().import_csv('final.csv')
#crash = Preprocessing().group_by_hour_by_day(crash)
crash = Preprocessing().group_data_give_quantity('borough', [],crash)
print(crash)
