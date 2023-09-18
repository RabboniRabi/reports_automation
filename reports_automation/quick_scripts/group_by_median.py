import sys
sys.path.append('../')

import pandas as pd
import numpy as np

import utilities.file_utilities as file_utilities

def group_agg_rename(df, grouping_levels, agg_dict:dict, append_str=''):
	"""
	Function to group data to given grouping levels, aggregating each data column 
	with its corresponding aggregation function given in the dictionary and
	renaming the columns to relect the aggregated nature of the data.

	Parameters:
	-----------
	df: Pandas DataFrame
		The data to group
	grouping_levels: list
		The list of columns to group the data upto (levels to group)
	agg_dict: dict
        The columns to aggregate and their corresponding functions
	append_st: str
		The string to append to the column name of each of the aggregate column

	Returns:
	-------
	The grouped data
	"""

	# Group and aggregate the data
	df_grouped = df.groupby(grouping_levels, as_index=False).agg(agg_dict)

	# Rename the columns to reflect the aggregated nature of the data
	cols_to_rename = {}
	for agg_col in agg_dict.keys():
		cols_to_rename[agg_col] = agg_col + '_' + agg_dict[agg_col] + '_' + append_str
	
	df_grouped.rename(columns=cols_to_rename, inplace=True)

	return df_grouped

grouping_levels = ['district_name', 'block_name',	'udise_code',	'school_name']
pivot_grouping_levels = ['District', 'Block', 'Schl_Category', 'Udise']


tenth_22_23_data_file_path = '/home/rabboni/Documents/EMIS/Data Reporting/reports/extracted/Aug_23/10th_board_stu_subj_wise_data_22_23.xlsx'
tenth_21_22_data_file_path = '/home/rabboni/Documents/EMIS/Data Reporting/reports/extracted/Aug_23/10th_board_stu_subj_wise_data_21_22.xlsx'

df_10th_22_23_report = pd.read_excel(tenth_22_23_data_file_path, sheet_name='stu_marks', skiprows=0)
df_10th_21_22_report = pd.read_excel(tenth_21_22_data_file_path, sheet_name='stu_marks', skiprows=0)
"""
df_total_grouped = df_report.groupby(grouping_levels, as_index=False).agg(tot_mean = ('total','mean'))

# Merge the school level mean back to the student level information
df_stu_det_w_mean = pd.merge(df_report, df_total_grouped, how='left', on=grouping_levels)

#df_stu_det_w_mean['below_average'] = df_stu_det_w_mean[df_stu_det_w_mean['total'] < df_stu_det_w_mean['tot_mean']] = 1
df_stu_det_w_mean['below_average'] = np.where(df_stu_det_w_mean['total'] < df_stu_det_w_mean['tot_mean'], 1, 0)
#df_stu_det_w_mean['above_average'] = df_stu_det_w_mean[df_stu_det_w_mean['total'] > df_stu_det_w_mean['tot_mean']] = 1
df_stu_det_w_mean['above_average'] = np.where(df_stu_det_w_mean['total'] > df_stu_det_w_mean['tot_mean'], 1, 0)

df_grouped_w_abv_bel_mean = df_stu_det_w_mean.groupby(grouping_levels, as_index=False).agg(
	no_stu_below_avg = ('below_average', 'sum'),
	no_stu_above_avg = ('above_average', 'sum'),
	no_stu = ('EMIS_NO', 'count')
)

df_grouped_w_abv_bel_mean['% below average'] = (df_grouped_w_abv_bel_mean['no_stu_below_avg'] / df_grouped_w_abv_bel_mean['no_stu']) 
df_grouped_w_abv_bel_mean['% above average'] = (df_grouped_w_abv_bel_mean['no_stu_above_avg'] / df_grouped_w_abv_bel_mean['no_stu']) """

# Group the data to school level, calculating the median and mean
"""df_grouped_10th_22_23 = df_10th_22_23_report.groupby(grouping_levels, as_index=False).agg(
	lang_median_22_23 = ('language','median'),
	eng_median_22_23 = ('english','median'),
	math_median_22_23 = ('maths','median'),
	sci_median = ('science','median'),
	soc_median = ('social','median'),
	tot_median = ('total','median')
	)"""


# Add average marks data
df_10th_22_23_report['avg'] = df_10th_22_23_report['total'] / 5
df_10th_21_22_report['avg'] = df_10th_21_22_report['total'] / 5

# Define the dictionary to aggregate the data on
tenth_data_agg_dict = {
	'language' : 'median',
	'english' : 'median',
	'maths' : 'median',
	'science' :'median',
	'social' : 'median',
	'avg': 'median'
}

# Group the data to school level
df_grouped_10th_22_23 = group_agg_rename(df_10th_22_23_report, grouping_levels, tenth_data_agg_dict, '22_23')
df_grouped_10th_21_22 = group_agg_rename(df_10th_21_22_report, grouping_levels, tenth_data_agg_dict, '21_22')

# Merge the two data sets
df_merged = pd.merge(df_grouped_10th_22_23, df_grouped_10th_21_22, how='left', on=grouping_levels)

# Compute and insert a difference column for language marks compared to last year
lang_cmp_prev_yr_series = df_merged['language_median_22_23'] - df_merged['language_median_21_22']
index = df_merged.columns.get_loc('language_median_22_23') + 1
df_merged.insert(index, 'lang_cmp_prev_yr', lang_cmp_prev_yr_series)

df_merged.to_excel('/home/rabboni/Documents/EMIS/Data Reporting/reports/extracted/Aug_23/10th_marks_schl_lvl.xlsx', sheet_name='10th_SCHL_LVL')


