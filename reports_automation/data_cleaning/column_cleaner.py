"""
Module to clean the column names
"""


import sys
sys.path.append('../')


import utilities.file_utilities as file_utilities
import pandas as pd
import re
def column_cleaning(df_report):



   #Declaring the patterns
   dist_pattern = re.compile("(?i)^dist(([\s\S]|)name(?=s$|$)|$)|^dist(?:rict([\s\S]|)name(?=s$|$)|(?:rict)$)")
   edu_dist_pattern = re.compile("(?i)^edu(?:cation|)([\s\S]|)dist(?:rict|)(([\s\S]|)name(?=s$|$)|$)")
   school_name_pattern = re.compile(("(?i)^school([\s\S]|)name(?=s$|$)|^school(?=s$|$)"))
   udise_pattern = re.compile("(?i)^udise([\s\S]|)code(?=s$|$)|^udise$")
   block_pattern = re.compile("(?i)^block([\s\S]|)name(?=s$|$)|^block$|^blk([\s\S]|)(?:name(?=s$|$)|$)")


   for col_name in df_report.columns:
       if re.search(dist_pattern, col_name):
           df_report.rename(columns={col_name: "district_name"}, inplace=True)
       elif re.search(edu_dist_pattern, col_name):
           df_report.rename(columns={col_name: "edu_dist_name"}, inplace=True)
       elif re.search(school_name_pattern, col_name):
           df_report.rename(columns={col_name: "school_name"}, inplace=True)
       elif re.search(udise_pattern, col_name):
           df_report.rename(columns={col_name: "udise_code"}, inplace=True)
       elif re.search(block_pattern, col_name):
           df_report.rename(columns={col_name: "block_name"}, inplace=True)
       else:
           continue
   return df_report


def main():
   # Ask the user to select the excel file to clean the columns.
   report = file_utilities.user_sel_excel_filename()
   df_report = pd.read_excel(report, sheet_name='Report', skiprows=4)
   column_cleaning(df_report)


if __name__ == "__main__":
   main()
