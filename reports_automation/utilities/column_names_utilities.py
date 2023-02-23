"""
Module with column name definitions
"""


# Column names are defined here so that they can be edited in one place

district_name = 'district_name'
district = 'District'
edu_district_name = 'edu_dist_name'
block_name = 'block_name'
block = 'Block'
udise_col = 'udise_code'
school_name ='school_name'
total_student_count  = 'total'
name = 'Name'
month_col = 'Month'
year_col = 'Year'
yes_col = 'Yes'
no_col = 'No'
management_type = "management_type"
category_type ="category_type"
distinct_udise_count = 'count(DISTINCT udise_code)'


school_category = 'category'
school_level = 'school_level'
class_number = 'class'
school_type = 'school_type'
un_aided = 'Un-aided'
central_govt = 'Central Govt'

tot_schools = 'Total Schools'

student_name = 'student_name'
cwsn_students ='cwsn'
beo_rank = 'BEO Rank'
deo = 'DEO'
beo = 'BEO'
deo_rank_elm = 'DEO Rank Elementary'
deo_rank_sec = 'DEO Rank Secondary'
perc_students_cp = '% Students ageing > 30 days'
total_cwsn_students ='cwsn'
emis_number = 'EMIS_Number'



# Common pool specific column names
students_ageing30_count = 'last_30days'
total_cp_students ='total'
ageing = 'ageing'
perc_ageing = '% ageing in CP'

# Health report specific column names
total = 'Total'
screened = 'Screened'
fully_comp = 'Fully Completed'
part_comp = 'Partially Completed'
not_started = 'Not started'
perc_screened = '% Screened'
perc_comp = '% Fully completed'


# CWSN report specific column names
cwsn_tot = 'Total CWSN Students'
cwsn_name = 'Name'
cwsn_in_School = 'In_School'
stdnts_in_school = 'Students in School'
cwsn_cp = 'Common Pool'
stdnts_in_cp = 'Students in Common Pool'
cwsn_schl_name = 'SchoolName'
cwsn_has_acct = 'HavingAccount'
cwsn_status = 'Student_Status'
nid = 'NID'
nid_count = 'NID Count'
udid = 'UDID'
udid_count = 'UDID Count'
with_acct = 'Students with account'
witht_acct = 'Students without account'
perc_students_with_UDID = '% Students with UDID'
perc_students_with_acct = '% Students with account'
stu_emis_no = 'Student_EMIS_NO'


# TPD report specific column names
tot_teachers = 'Total_Teachers'
train_attnd = 'Traning_Attended'

# PET to school mapping specific column names
mapping_status = 'Mapping Status'
fully_mapped = 'Fully Mapped School'
part_mapped = 'Partially Mapped School'
perc_fully_mapped = '% Fully mapped'


# Ennum Ezhuthum related column names
perc_asses_comp = '% Summative Assessment Completion'


# Kalai thiruvizha specific column
participants = 'Participations'
tot_students = 'Total Students'
per_participants = '% Student participations'

# Palli Parvai specific column names
observation_date = 'Date of Observation'
observed_by = 'Observed by'
designation_user_id = 'Observed by'
pp_designation = 'stackholders'
deo_target = 'deo_target'
ceo_target ='ceo_target'
perc_DEO_obs = '% School Observations by DEOs'
perc_CEO_obs = '% School Observations by CEOs'
perc_obs_comp = '% Overall Observation Completion'

# BRC-CRC mapping specific column names
beo_user = 'beo_user'
beo_name ='beo_name'
deo_name_elm = 'deo_name (elementary)'
deo_name_sec = 'deo_name (secondary)'
school_level = 'school_level'


# Report specific column names
elem_schl_lvl = 'Elementary School'
scnd_schl_lvl = 'Secondary School'


# OoSC report specific column names
reason_type = 'Reason_type'
to_be_surveyed = 'To be surveyed'
perc_to_be_admitted = '% to be admitted'
perc_admitted_oosc = '% Students Admitted' 
to_be_admitted = 'To be admitted'
oosc_student_status = 'student_status'
not_admttd = 'Not Admitted'
to_be_verified = 'To be verified'
non_target = 'Non-Target'
stdnt_admttd = 'Student Admitted'
stdnts_admttd = 'Students Admitted'
oosc_tot_surveyed = 'Total Surveyed'

# Hi-tech lab report specific column names
up_time_hrs = 'up_time_hrs'
mediam_up_time_hrs = 'Median Uptime Hours'

# Library specific column names
tot_secs = 'Total_Sections'
total_tchrs = 'Total Teachers'
tchrs_assigning_books = 'Teachers assigning books'
tchrs_not_assigning_books = 'Teachers not assigning books'
perc_tchrs_assigning_books = '% Teachers assigning books'
shelves_created = 'No_of_Section_created_shelves'
shelves_not_created = 'No_of_Section_Not_created_shelves'
perc_shelves_created = '% Shelves created'
class_teacher_id = 'class_teacher_id'
book_assigning_status = 'Book_Assigning_Status'
books_not_assigned = 'Books Not Assigned'
books_assigned = 'Books Assigned'


# Attendance specific column names
tot_tchrs = 'Total_teachers'
updt_tchrs = 'Updated_Teachers'
appld_tchrs = 'Applied_Teachers'
perc_tchrs_updated = '% Updated'
per_tchrs_applied = '% Applied'
tot_marked_schls = 'Total Marked Schools'
marked_schools = 'Marked Schools'
unmarked_schools = 'Unmarked Schools'
tot_unmarked_schls = 'Total Unmarked Schools'
perc_marked_schls = '% Marked'
tot_marked = 'totalmarked'
tot_unmarked = 'totalunmarked'
perc_7_days_unmarked_schls = '% Unmarked Schools for 7 days'


# Updation specific column names
up_tot_tchrs = 'total_teachers'
not_updt_tchrs = 'notupdated_teachers'
perc_not_updt = '% Not Updated'

# Ranking specific column names
desig = 'Designation'
metric_code = 'metric_code'
metric_category = 'metric_category'
rank_col = 'Rank'
ranking_value = 'Ranking Value'
ranking_value_desc = 'Ranking Value Description'
beo_rank = 'BEO Rank'
deo_elem_rank = 'DEO (Elementary) Rank'
deo_sec_rank = 'DEO (Secondary) Rank'

# Sports specific column names
test_comp_status = 'Completion Status'
test_in_progress = 'In Progress'
test_completed = 'Completed'
test_not_started = 'Not Yet Started'
sports_tot_stu = 'Total_Students'
m50_comp_stu = '50m Completed_Students'
m600_800_comp_stu = '600/800m Completed_Students'
shuttle_comp_stu = '6*10m shuttle Completed_Students'
kg4_shot_comp_stu = '4kg shotput Completed_Students'
long_jump_comp_stu = 'Longjump Completed_Students'
perc_test_comp = '% Completed'
perc_50m_comp = '% 50M completed'
perc_600m_800m_comp = '% 600/800M completed'
perc_6_10m_shutt_comp = '% 6*10M shuttle completed'
perc_4kg_shot_comp = '% 4kg shotput completed'
perc_long_jump_comp = '% long jump completed'
perc_avg_overall_comp = 'Average % of tests completed'

# G2C pending applications
tot_app_rcvd = 'Total_applications_received'
tot_aprvd = 'Total_Approved'
tot_pnding = 'Total_Pending'
tot_rjctd = 'Total_Rejected'
tot_pnd_grtr_15_days = 'Pending_more_than_15days'
tot_pnd_lessr_15_days = 'Pending_less_than_15days'
perc_apps_grtr_15_days = '% Pending_more_than_15days'


# Welfare schemes specific columns
scheme_status = 'status'
scheme_inprogress = 'inprogress'
scheme_in_progress = 'In Progress'
scheme_comp = 'completed'
scheme_completed = 'Completed'
scheme_nt_strt = 'not started'
scheme_not_started = 'Not Started'
perc_schools_issued_books = '% schools completed book issue'






def get_value(var_name: str):
    """
    Function to get the value mapped to the variable defined here.
    This function is used to fetch the value when the 
    variable name gets coverted to string (when reading from JSON)
    
    Parameters:
    ----------
    var_name: str
        The name of the variable to look up the value for
    Returns:
        The value mapped to the variable    
    """

    # Remove module part of variable name if it exists
    module_import_name = 'cols.'
    if (module_import_name in var_name):
        var_name = var_name.removeprefix(module_import_name)
    
    # Get the value mapped to the variable
    value = globals()[var_name]
    return value

def get_values(var_names_list: list):
    """
    Function to get the values for string list of variable names.

    This function is usef to fetch the values when the 
    variable names get converted to strings (When reading from JSON)

    Parameters:
    ----------
    var_names_arr: list
        List of variable names of strings whose values need to be fetched
    Returns:
    --------
        List of values corresponding to given list of string variable names
    """
    values = []
    for var_name in var_names_list:
        value = get_value(var_name)
        values.append(value)
    return values


def update_dictionary_var_strs(var_names_keys_dict: dict):
    """
    Function to update the keys in a given dictionary.
    The keys are strings of variable names and will be updated
    by mapping to the value assigned to the variable names.

    Parameters:
    -----------
    var_names_keys_dict: dict
        Dictionary whose keys (which are strings of variables) need to be updated with
        the values of the variable names
    
    Returns:
    -------
    The updated dictionary
    """

    updated_dict = {}

    for key in var_names_keys_dict.keys():
        dict_key_value = var_names_keys_dict[key]
        updated_key = get_value(key)

        # Set the updated key-value pair
        updated_dict[updated_key] = dict_key_value

    return updated_dict
