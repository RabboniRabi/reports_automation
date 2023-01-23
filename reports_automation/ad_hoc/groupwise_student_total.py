"""
Script written to get school wise count of 11th & 12th students studying
Biology, Pure Science, Computer Science, Computer Application, Computer Technology
in Chengalpattu and Chennai districts

Hoping this script will be useful in future by editing some of the parameters
"""

import utilities.utilities as utilities


# File path to the report
file_path = r'/home/rabboni/Downloads/Grpwise-Mediumwise-Report.xlsx'
geog_classification_file_path = r'/home/rabboni/Documents/EMIS/Data Reporting/reports/schools_urban_rural_classfication.xlsx'


def dist_class_group_filtered_students_count():
    """
    Function to filter the groupwise data of all school students
    district wise, class wise, group wise.
    """

    # Districts to filter
    districts = ['CHENGALPATTU', 'CHENNAI']
    # School types to filter
    school_types = ['Government']
    # Groups to filter
    groups = [2503, 2608, 2502, 2702, 2802]
    # Columns to save
    columns = ['DistrictName', 'BlockName', 'EduDistrictName', 'UDISE',	'SchoolName', 'SchoolType', 'GroupCode', 'GroupName', 'Medium', 'Cls_11_Total', 'Cls_12_Total']

    # Load the report as a pandas data frame object
    df_grp_wise_rpt = utilities.read_sheet(file_path, 'Report')

    # Filter districts
    df_grp_wise_rpt_filtered_dist = utilities.filter_dataframe_column(df_grp_wise_rpt, 'DistrictName', districts)

    # Filter by group codes
    df_grp_wise_rpt_filtered_dist_grp = utilities.filter_dataframe_column(df_grp_wise_rpt_filtered_dist,'GroupCode', groups)

    # Filter by school type
    df_grp_wise_rpt_filtered_dist_grp_schl = utilities.filter_dataframe_column(df_grp_wise_rpt_filtered_dist_grp,'SchoolType', school_types)

    
    df_grp_wise_rpt_for_save = utilities.columns_subset(df_grp_wise_rpt_filtered_dist_grp_schl, columns)

    # Rename columns for better readability
    df_grp_wise_rpt_for_save.rename(columns = {'Cls_11_Total':'Class 11 students','Cls_12_Total':'Class 12 students'}, inplace = True)

    # Save the modified data frame to excel
    utilities.save_to_excel(df_grp_wise_rpt_for_save, 'school_grp_student_count.xlsx', 'Report')


def low_student_count(student_count_threshold, location_classification, class_column_name, desired_col_name, file_name):
    """
    Function to get data of schools where students in a group are less than a given threshold number
    The data is filtered to given location classification: Urban/Rural
    """

    # School types to filter
    school_types = ['Government']
    # Columns to save
    columns = ['DistrictName', 'BlockName', 'EduDistrictName', 'UDISE',	'SchoolName', 'SchoolType', 'GroupCode', 'GroupName', 'Medium', 'Cls_12_Total']
    

    # Load the data containing Rural/Urban classification of schools as a data frame object
    df_geo_classif = utilities.read_sheet(geog_classification_file_path, 'location_classification')

    # Filter schools with given location classification
    df_geo_filtered = utilities.filter_dataframe_column(df_geo_classif, 'Location', [location_classification])

    # Load the group wise report as a pandas data frame object
    df_grp_wise_rpt = utilities.read_sheet(file_path, 'Report')

    # Filter by school type
    df_grp_wise_rpt_schl = utilities.filter_dataframe_column(df_grp_wise_rpt,'SchoolType', school_types)


    # Get the intersection of school data with goup wise report and schools with location_classification
    df_geo_classif_merged = df_grp_wise_rpt_schl.merge(df_geo_filtered[['UDISE', 'Location']])

    # Get the schools whose students in a group/class is less than the given threshold
    df_lower_than_threshold = utilities.filter_column_le(df_geo_classif_merged, class_column_name, student_count_threshold)

    # Select a subset of columns to save for final report
    df_lower_than_threshold_for_save = utilities.columns_subset(df_lower_than_threshold, columns)

    # Rename column for better readability
    df_lower_than_threshold_for_save.rename(columns = {class_column_name:desired_col_name}, inplace = True)

    # Save the modified data frame to excel
    utilities.save_to_excel(df_lower_than_threshold_for_save, file_name, 'Report')






# Main function to call the specific function
def main():
    
    # Function that count of students in schools filtered district, class & group wise
    #dist_class_group_filtered_students_count()

    low_student_count(30, 'Urban', 'Cls_12_Total', 'Class 12 Students', 'urban_schools_le_30_student_strength.xlsx')
    low_student_count(15, 'Rural', 'Cls_12_Total', 'Class 12 Students', 'rural_schools_le_15_student_strength.xlsx')



if __name__ == "__main__":
    main()