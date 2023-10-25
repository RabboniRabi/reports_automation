"""
Quick script to merge latitude and longitude values with board results data
"""

import pandas as pd

import sys
sys.path.append('../')


districts_lat_long_path = '/home/rabboni/Downloads/district_lat_long.xlsx'

file_name = 'HSC_urbanrural_subj_wise_rpt.xlsx'

file_path = '/home/rabboni/Downloads/' + file_name

import utilities.file_utilities as file_utilities


def merge_lat_long_with_dist_level_data():
    """
    """
    districts_lat_long = pd.read_excel(districts_lat_long_path, sheet_name='dist_lat_long', skiprows=0)

    dist_lvl_data = pd.read_excel(file_path, sheet_name='District', skiprows=0)

    # Merge the data
    dist_lvl_data_w_lat_long = pd.merge(dist_lvl_data, districts_lat_long, how='left', on='district_name')

    dir_path = file_utilities.get_curr_day_month_gen_reports_dir_path()
    file_utilities.save_to_excel({'District': dist_lvl_data_w_lat_long}, file_name, dir_path)


if __name__ == '__main__':
    merge_lat_long_with_dist_level_data()

