"""
Module to create a report for teacher with their classes and subject details.
"""
import sys

sys.path.append('../')
import pandas as pd
import utilities.file_utilities as file_utilities



def all_teach_sub_det_1_10(mang_typ_list_df: list, classes: list):
    """
     Function to get the teacher details with their subjects for classes 1 to 10

    Parameters:
    -----------
    mang_typ_list_df: list
        The list of different school management type

    classes: list
        The list of different groups of classes (1-3,4-5..)

    Returns:
    -------
         pd.Dataframe
        Dataframe with the teacher mapped to their subject
    """

    # Initialise an empty dataframe
    all_manag_typ_master_df = pd.DataFrame()

    for df in mang_typ_list_df:
        # For each management type data

        # Drop out the sections column as details are only needed at class level
        if 'section' in df.columns:
            df.drop(columns='section', axis=1, inplace=True)

        # Remove Duplicates
        df = df.drop_duplicates()

        # Filter the dataframe for the given list of classes
        df = df.loc[df['class_id'].isin(classes)]

        # Pivot table to map teacher with their subjects
        teacher_sub_det = pd.pivot_table(df, index=['district_name', 'block_name', 'udise_code', 'school_name',
                                                    'school_type', 'management', 'cate_type', 'teacher_id',
                                                    'teacher_name', 'class_id'],
                                         columns='subjects', values='subject_id', fill_value=0,
                                         aggfunc='count').reset_index()

        # Concatenate to get different school management type in a single data frame
        all_manag_typ_master_df = pd.concat([all_manag_typ_master_df , teacher_sub_det])

    # Denote empty cells by NA
    all_manag_typ_master_df.fillna('NA', inplace=True)

    return all_manag_typ_master_df

def all_teach_sub_det_11_12(mang_typ_list_df: list, classes: list):
    """
     Function to get the teacher details with their subjects for 11 and 12 classes

    Parameters:
    ___________
        mang_typ_list_df: list
           The list of different school management type

        classes: list
           The list of groups of classes

    Returns:
    ___________
           pd.Dataframe
           The Dataframe with the teacher mapped to their subject

    """
    # Initialise an empty dataframe
    all_manag_typ_master_df = pd.DataFrame()

    for df in mang_typ_list_df:
        # For each management type data

        # Drop out the sections column as details are only needed at class level
        if 'section' in df.columns:
            df.drop(columns=['section'], axis=1, inplace=True)

        # Removing Duplicates
        df = df.drop_duplicates()

        # filter the dataframe for the given list of class
        df = df.loc[df['class_id'].isin(classes)]

        # Concatenating to get different school management type in a single data frame
        all_manag_typ_master_df = pd.concat([all_manag_typ_master_df, df])

    return all_manag_typ_master_df

def main():
    """
    Generate report with teacher details and their undertaking subjects
    """
    # Get Unaided school data
    df_unaid = pd.read_excel(r'C:\Users\TAMILL\tch\tch_class_sub_un.xlsx')
    print("Read sucessfully")

    # Partially aided df
    df_part_aid = pd.read_excel(r'C:\Users\TAMILL\tch\tch_class_sub_part.xlsx')
    print("Read sucessfully")

    # Fully aided df
    df_full_aid = pd.read_excel(r'C:\Users\TAMILL\tch\tch_class_sub_full.xlsx')
    print("Read sucessfully")

    # Central govt df
    #df_cent = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\teacher_detials\central.xlsx')

    # Govt schools df as 4 datasets due to large size of the data
    df_govt_1 = pd.read_excel(r'C:\Users\TAMILL\tch\tch_class_sub_govt1.xlsx',sheet_name= 'ar_kar')
    print("Read sucessfully")
    df_govt_2 = pd.read_excel(r'C:\Users\TAMILL\tch\tch_class_sub_govt1.xlsx',sheet_name= 'kr_ten')
    print("Read sucessfully")
    df_govt_3 = pd.read_excel(r'C:\Users\TAMILL\tch\tch_class_sub_govt2.xlsx')
    print("Read sucessfully")

    # Declare list of all school types
    all_manag_type = [df_unaid, df_part_aid, df_full_aid, df_govt_1, df_govt_2, df_govt_3]

    # List of group of classes
    classes_list = [[1, 2, 3], [4, 5], [6, 7, 8],[9, 10],[11,12]]

    # Path to be saved
    directory_path = file_utilities.get_curr_day_month_gen_reports_dir_path()

    # Generate & save report for different sets of classes

    # For classes 1 to 3
    df_class_1_3 = all_teach_sub_det_1_10(all_manag_type, classes_list[0])
    file_utilities.save_to_excel({'Report':df_class_1_3 },'class_1_3.xlsx', dir_path=directory_path)

    # For classes 4 and 5
    df_class_4_5 = all_teach_sub_det_1_10(all_manag_type,classes_list[1])
    file_utilities.save_to_excel({'Report':df_class_4_5 },'class_4_5.xlsx', dir_path=directory_path)

    # For classes 6 to 8
    df_class_6_8 = all_teach_sub_det_1_10(all_manag_type, classes_list[2])
    file_utilities.save_to_excel({'Report':df_class_6_8 },'class_6_8.xlsx', dir_path=directory_path)

    # For classes 9 and 10
    df_class_9_10 = all_teach_sub_det_1_10(all_manag_type, classes_list[3])
    file_utilities.save_to_excel({'Report':df_class_9_10 },'class_9_10.xlsx', dir_path=directory_path)

    # For classes 11 and 12
    df_class11_12= all_teach_sub_det_11_12(all_manag_type, classes_list[4])
    file_utilities.save_to_excel({'Report':df_class11_12 },'class_11_12.xlsx', dir_path=directory_path)
 


if __name__ == "__main__":
    main()
