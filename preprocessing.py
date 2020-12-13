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

    def injured_killed(self, crash):
        """This function will create a column which say if there is injured or not and killed or not"""

        crash['injured'] = crash['number_of_persons_injured'].apply(lambda x : "yes" if x else "no")
        crash['killed'] = crash['number_of_persons_killed'].apply(lambda x : "yes" if x else "no")

        return crash

    def injured_killed_by_borough(self, crash):
        """will return quantity of injured and killed by borough"""

        crash = Preprocessing().injured_killed(crash)
        crash['injured'] = pd.get_dummies(crash['injured'], prefix='injured', drop_first="True")
        crash['killed'] = pd.get_dummies(crash['killed'], prefix='killed', drop_first="True")
        crash = Preprocessing().group_data('borough',['injured', 'killed'], crash, False)

        return crash

    def number_of_vehicule(self, crash):
        """Will calculate number of contributing factor by accident and the number of vehicule"""

        crash["contributing_factor_vehicle_1"] = crash['contributing_factor_vehicle_1'].apply(lambda x: 0 if x == 'Unspecified' else 1)
        crash["contributing_factor_vehicle_2"] = crash['contributing_factor_vehicle_2'].apply(lambda x: 0 if x == 'Unspecified' else 1)
        crash["contributing_factor_vehicle_3"] = crash['contributing_factor_vehicle_3'].apply(lambda x: 0 if x == 'Unspecified' else 1)
        crash["contributing_factor_vehicle_4"] = crash['contributing_factor_vehicle_4'].apply(lambda x: 0 if x == 'Unspecified' else 1)
        crash["contributing_factor_vehicle_5"] = crash['contributing_factor_vehicle_5'].apply(lambda x: 0 if x == 'Unspecified' else 1)
        crash['number_of_vehicule'] = (crash["contributing_factor_vehicle_1"] + crash["contributing_factor_vehicle_2"] +
                                        crash["contributing_factor_vehicle_3"] + crash["contributing_factor_vehicle_4"] +
                                        crash["contributing_factor_vehicle_5"])

        return crash
    
    def group_number_of_vehicul_by_x(self, crash, groupby_value, mean = True):
        """Will group by the value that we want with the sum or mean number of vehicule got in accident"""

        crash = Preprocessing().number_of_vehicule(crash)
        wanted_list = ['crash_date','crash_time', 'borough', 'zip_code', 'latitude', 
                'longitude', 'location', 'on_street_name', 'off_street_name',
                'cross_street_name', 'number_of_persons_injured','number_of_persons_killed','number_of_pedestrians_injured',
                'number_of_pedestrians_killed','number_of_cyclist_injured','number_of_cyclist_killed',
                'number_of_motorist_injured','number_of_motorist_killed',
                'collision_id', 'vehicle_type_code1', 'vehicle_type_code2', 
                'vehicle_type_code_3', 'vehicle_type_code_4', 'vehicle_type_code_5']
        wanted_list.remove(groupby_value)
        crash.drop(wanted_list, axis = 1, inplace = True)

        if mean:
            crash = crash.groupby(crash[groupby_value]).mean()
        else:
            crash = crash.groupby(crash[groupby_value]).sum()
        return crash


crash = Cleaning().import_csv('final.csv')
#crash = Preprocessing().group_by_hour_by_day(crash)
#crash = Preprocessing().group_data('borough', [], crash)
#crash = Preprocessing().injured_killed_by_borough(crash)
#crash = Preprocessing().number_of_vehicule(crash)
crash = Preprocessing().group_number_of_vehicul_by_x(crash, 'borough', True)

print(crash)