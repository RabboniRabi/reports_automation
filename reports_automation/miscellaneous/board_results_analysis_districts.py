"""
Module with functions to create a report card/analysis of schools' performance
in 10th and 12th board exams with data compared to previous year and split
up district wise.
"""

import pandas as pd








# Testing formatting in XLSX writer

writer = file_utilities.get_xlsxwriter_obj(
	{'10th_SCHL_LVL': df_merged}, 
	'10th_marks_schl_lvl.xlsx',
	file_path='/home/rabboni/Documents/EMIS/Data Reporting/reports/extracted/Aug_23/')


writer.sheets['10th_SCHL_LVL'].conditional_format('F2:F5613', {'type': 'icon_set',
                                                         'icon_style': '3_arrows',
                                                         'icons': [
                  {'criteria': '>', 'type': 'number', 'value': '0'},
                  {'criteria': '==', 'type': 'number', 'value': '0'}
                                                         ]}
                                            )



print('saving sheeting after formatting')
writer.save()




