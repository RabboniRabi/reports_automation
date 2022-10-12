"""
Module to create common pool ranking report by doing the following manipulations
to the downloaded report from dashboard
 - Pivot the table to get class wise aggregates
"""

import pandas as pd
import utilities.utilities as utilities
import sys


# Global variables
# Column names are defined here so that they can be edited in one place
student_count  = 'count(distinct unique_id_no)'
blockwise_student_count = 'count(distinct h.unique_id_no)'
district_name = 'district_name'
edu_district_name = 'edu_dist_name'
block_name = 'block_name'
class_number = 'Class'
moved_cp = 'Moved to CP'
grand_total = 'Grand Total'

tmp_file_path = r'/home/rabboni/Downloads/commonpool_classwise_report (14).xlsx'

def main():
    """
    Main function to execute functionality of this module
    """
    #file = utilities.user_open_file()
    #path = file.name
    # Directly supplying path for now to skip selecting file during testing
        
    df_data = utilities.read_sheet(tmp_file_path, 'Report', skiprows=4)
    df_blockwise = utilities.read_sheet(tmp_file_path, 'Abstract')

    # Convert all header value types to string
    df_data.columns = df_data.columns.map(str)

    # Pivot the table to get class wise count of students in common pool aggregated at block level
    df_classwise_pivot = pd.pivot_table(df_data, values=student_count, index=[district_name, edu_district_name, block_name],
                    columns=[class_number], aggfunc='sum').reset_index()

    
    # Add the class wise count of students at block level to get total count of students in common pool in a block
    # Put the totals in a new column. Skip the first 3 columns in this sum as they are text
    df_classwise_pivot[grand_total]  = df_classwise_pivot.iloc[:, 3:].sum(axis=1)

    # In data frame containing blockwise summary, rename the column: count(distinct h.unique_id_no) to Moved to CP
    df_blockwise.rename(columns = {blockwise_student_count:moved_cp}, inplace = True)

    # Inner join data in the two data frames on the intersection of the columns district_name, edu_dist_name, block_name
    # This merge will effectively include the 'Moved to CP' column to the data set,
    # skipping rows that not present in both places
    df_blockwise_merged = df_classwise_pivot.merge(df_blockwise[[district_name, edu_district_name, block_name, moved_cp]])

    # Calculate the % of students moved to the common pool by using data in 'Grand total' and 'Moved to CP' columns
    df_blockwise_merged['% in Common Pool'] = df_blockwise_merged[grand_total]/df_blockwise_merged[moved_cp]

    # Create blockwise ranking based on % in common pool values
    df_blockwise_merged['Rank'] = df_blockwise_merged['% in Common Pool'].rank(ascending=True, method='min')

    # Calculation of Ranking for Educational Districts
    # 1. Group data to the level of educational district (This removes further sub-classifications such as block). 
    # 2. Calculate the values of 'Grand Total' and 'Moved to CP' for each of the educational districts
    # by doing a sum of values grouped to educational district level
    df_ed_rank = df_blockwise_merged.groupby([edu_district_name])[[grand_total, moved_cp]].sum()
    # 3. Rank based on fraction moved to CP
    df_ed_rank['EDist_Data'] = (df_ed_rank[grand_total]/df_ed_rank[moved_cp])
    df_ed_rank['EDist_Rank'] = df_ed_rank['EDist_Data'].rank(ascending=True, method='min')
    df_ed_rank = df_ed_rank.reset_index()

    # Ranking for District similar to Educational Districts
    df_dist_rank = df_blockwise_merged.groupby([district_name])[[grand_total, moved_cp]].sum()
    df_dist_rank['Dist_Data'] = (df_dist_rank[grand_total]/df_dist_rank[moved_cp])
    df_dist_rank['Dist_Rank'] = df_dist_rank['Dist_Data'].rank(ascending=True, method='min')
    df_dist_rank = df_dist_rank.reset_index()

    # Vlookup for educational district ranks based on name
    df_blockwise_merged['ERank'] = df_blockwise_merged[edu_district_name].\
     apply(utilities.xlookup, args=(df_ed_rank[edu_district_name], df_ed_rank['EDist_Rank']))

    # Vlookup for district ranks based on name
    df_blockwise_merged['DRank'] = df_blockwise_merged[district_name].\
     apply(utilities.xlookup, args=(df_dist_rank[district_name], df_dist_rank['Dist_Rank']))

    # Convert values to percentage and upto two decimal places
    df_blockwise_merged.loc[:, "% in Common Pool"] = df_blockwise_merged["% in Common Pool"].map('{:.2%}'.format)

    # Sort by columns
    df_blockwise_merged = df_blockwise_merged.sort_values(['DRank', district_name, 'ERank', edu_district_name, 'Rank'],
                      ascending=[True, True, True, True, True])

    df_blockwise_merged_dict = {'Test':df_blockwise_merged}
    utilities.save_to_excel(df_blockwise_merged_dict,'df_blockwise_merged_dict.xlsx')                   

    #Testing
    df_blockwise_merged.columns = df_blockwise_merged.columns.map(str)
    df_blockwise_merged_pivot = utilities.pivot_table_w_subtotals(df_blockwise_merged \
                        , values=[moved_cp,grand_total, '1','2','3']
                        , indices=['district_name', 'edu_dist_name', 'block_name'] \
                        , aggfunc='sum',columns=[''],fill_value='').reset_index()

    """# Creating View for "Total View" for Edu Dist
    # Create a new data frame object with only one initial column containing educational district names
    TV_ED = pd.DataFrame(df_blockwise_merged[edu_district_name])

    # Lookup rank of each district in TV_D['district_name] and put it in a new column: 'ERank' in the data frame object
    TV_ED['ERank'] = TV_ED[edu_district_name]. apply(utilities.xlookup, args=(ed_rank['edu_dist_name'], ed_rank['EDist_Rank']))

    # Add the string total to each district name
    TV_ED[edu_district_name] = TV_ED[edu_district_name] + ' Total'

    # Drop duplicate values
    TV_ED = TV_ED.drop_duplicates(keep='first')

    # Creating View for "Total View" for Dist

    # Create a new data frame object with only one initial column containing district names
    TV_D = pd.DataFrame(df_f['district_name'])

    # Lookup rank of each district in TV_D['district_name] and put it in a new column: 'DRank' in the data frame object
    TV_D['DRank'] = TV_D['district_name']. apply(xlookup, args=(d_rank['district_name'], d_rank['Dist_Rank']))

    # Add the string total to each district name
    TV_D['district_name'] = TV_D['district_name'] + ' Total'

    # Drop duplicate values
    TV_D = TV_D.drop_duplicates(keep='first')    

    # Remove last 2 columns (ERank & DRank) - these were used for merge and sort in previous steps
    df_blockwise_merged.drop(columns=df_blockwise_merged.columns[-2:],
        axis=1,
        inplace=True)      """ 


    # Intermediate saves for testing
    df_sheet_dict = {'Test':df_blockwise_merged_pivot}
    utilities.save_to_excel(df_sheet_dict,'test.xlsx')    

    
    



if __name__ == "__main__":
    main()
