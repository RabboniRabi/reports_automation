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


school_category = 'category'
school_level = 'school_level'
class_number = 'class'
school_type = 'school_type'
un_aided = 'Un-aided'
central_govt = 'Central Govt'

tot_schools = 'Total Schools'

cwsn_students ='cwsn'
beo_rank = 'BEO Rank'
deo_rank_elm = 'DEO Rank Elementary'
deo_rank_sec = 'DEO Rank Secondary'
perc_students_cp = '% Students ageing > 30 days'
total_cwsn_students ='cwsn'



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


# BRC-CRC mapping specific column names
beo_user = 'beo_user'
beo_name ='beo_name'
deo_name_elm = 'deo_name (elementary)'
deo_name_sec = 'deo_name (secondary)'
school_level = 'school_level'


# Report specific column names
elem_schl_lvl = 'Elementary School'
scnd_schl_lvl = 'Secondary School'


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

    for key in var_names_keys_dict.keys():
        dict_key_value = var_names_keys_dict[key]
        updated_key = get_value(key)

        # Set the updated key-value pair
        var_names_keys_dict[updated_key] = dict_key_value

        # Remove the older key-value pair
        var_names_keys_dict.pop(key)

    return var_names_keys_dict
