# nyc-crashes
![Analysis](https://www.nyc.fr/wp-content/uploads/2015/07/New_York_City.jpg)
# What

We create a program that use a data set of vehicle crash in New-York city and we clean the data and try to do some preprocessing.

# Why

We are doing this exercise during our training to better understand cleaning and preprocessing.

# When

On December 2020, this exercise took us around 3 days.

# How

We use Pandas and numpy to do this project.

If you want to use this project, you need to have these libraries and python 3 and then you just need to clone.

You will have the data set in the csv fil named data_100000.csv and the cleaned data in final_csv.
We are doing only general cleaning. On cleaning.py we have these functions:

- import_csv: will import data from csv file as dataframe
- change_type: will change the type of columns to datatime or integer.
- cleanin_space: will delete unnecessary space of value
- replace_NaN_value: will replace NaN value by Unspecified if the type is string and -1 if integer
- delete_duplicated: will delete duplicate value
- create_final_csv: will create final.csv file

We also have 2 functions (check_value_long_lat_and_change and finding_missing_value) that are not used because we didn't have enough time. These 2 functions do reverse geocoding to find missing value of zip_code. To use this function you need to import Nominatim from geopy.

Since we did not know what we will do with our values, we preferred to remain general by doing only these cleaning functions.

On preprocessing.py we create these functions:

- group_by_hour_by_day: will group crash by week day by hour and will return mean value of all other columns.
- group_data: more general function that will group by column that we want and will give us mean or sum of the column that we want.
- injured_killed: will return yes or no by accident if there is injured person and killed people.
- injured_killed_by_borough: will call injured_killed function change value by 1 or 0 and then will group by borough and do the sum.
- number_of_vehicule: will give number of vehicles that got into accident
- group_number_of_vehicul_by_x: will group number of vehicule that got into accident by what we want. It can do sum or mean.

# Who

[Ebubekir Kocadag](https://github.com/EbubekirKocadag), junior AI developer

# Pending things to do

Like we already said, we can continue to improve reverse geocoding and replace value of zip code, borough, street name etc by something better than -1 or Unspecified. We can also add new function like normalization or others...
