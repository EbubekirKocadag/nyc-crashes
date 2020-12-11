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

    def group_data(self, groupby_value: str, wanted_list: list, crash, mean: bool = True):
        """General function which with given column that we want to group with the list of column name that
        we want to take mean value. It will give quantity of grouped value too
        if mean True will give mean, if not will give sum of wanted_list"""

        columns = list(crash.columns)
        wanted_list.append(groupby_value)
        final_list = []

        for i in columns:
            if i not in wanted_list:
                final_list.append(i)
        crash.drop(final_list, axis= 1, inplace= True)

        if mean:
            """We will group by groupby and add quantity column"""
            crash['quantity'] = 1
            quantity = crash['quantity'].groupby(crash[groupby_value]).sum()
            crash = crash.groupby(crash[groupby_value]).mean()
            crash['quantity'] = quantity
        else:
            crash = crash.groupby(crash[groupby_value]).sum()
        return crash

    def injuried_killed(self, crash):
        """This function will create a column which say if there is injuried or not and killed or not"""

        crash['injuried'] = (crash['number_of_persons_injured'] + crash['number_of_pedestrians_injured'] 
                             + crash['number_of_cyclist_injured'] + crash['number_of_motorist_injured'])
        crash['injuried'] = crash['injuried'].apply(lambda x : "yes" if x else "no")
        crash['killed'] = (crash['number_of_persons_killed'] + crash['number_of_pedestrians_killed'] 
                             + crash['number_of_cyclist_killed'] + crash['number_of_motorist_killed'])
        crash['killed'] = crash['killed'].apply(lambda x : "yes" if x else "no")

        return crash

    def injuried_killed_by_borough(self, crash):
        """will return quantity of injuried and killed by borough"""

        crash = Preprocessing().injuried_killed(crash)
        crash['injuried'] = pd.get_dummies(crash['injuried'], prefix='injuried', drop_first="True")
        crash['killed'] = pd.get_dummies(crash['killed'], prefix='killed', drop_first="True")
        crash = Preprocessing().group_data('borough',['injuried', 'killed'], crash, False)

        return crash

crash = Cleaning().import_csv('final.csv')
#crash = Preprocessing().group_by_hour_by_day(crash)
#crash = Preprocessing().group_data('borough', [], crash)
crash = Preprocessing().injuried_killed_by_borough(crash)
print(crash)
