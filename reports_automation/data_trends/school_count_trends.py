"""

Module with functions to:
- Update records of total schools count for each day the script is run on.
- Collate and track UDISE codes for each day the script is run on.

"""

def main():
    # Read the database connection credentials
    credentials_dict = dbutilities.read_conn_credentials('db_credentials.json')

    # Get the latest students and teachers count
    df_report = fetch_data_as_df(credentials_dict, 'students_school_child_count_summary.sql')

    # Alternatively
    # Ask the user to select the School enrollment abstract excel file.
    #school_enrollment_abstract = file_utilities.user_sel_excel_filename()
    #df_report = pd.read_excel(school_enrollment_abstract, sheet_name='Report', skiprows=0)


    # district wise count of schools based on UDISE code - Separate function for this

    # UDISE day wise tracking (present/absent) - Separate function for this




if __name__ == "__main__":
    main()