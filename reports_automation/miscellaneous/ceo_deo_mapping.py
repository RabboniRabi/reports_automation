"""
Script to create a CEO - DEO mapping dictionary from BRC-CRC mapping data
"""

import sys
sys.path.append('../')

import utilities.utilities as utilities
import utilities.file_utilities as file_utilities
import utilities.column_names_utilities as cols

import json

def get_ceo_deo_mapping():
    """
    Function to get the DEOs to CEO mapping from the BRC CRC mapping data

    Returns:
    --------
    Dictionary of the CEO to DEO mapping
    """

    # Fetch the BRC CRC mapping data
    mapping_data_dir_path = file_utilities.get_mapping_data_dir_path()
    file_path = file_utilities.get_file_path('BRC_CRC_Master_V3.xlsx', mapping_data_dir_path)

    df_brc_crc_mapping = file_utilities.read_sheet(file_path, sheet_name='BRC-CRC V3 wo hyphen')

    ceo_deo_mapping = {}

    # Get the list of unique CEOs (districts)
    ceos = df_brc_crc_mapping[cols.district_name].unique()

    # For each ceo, get the unique DEO Elementary and Secondary
    for ceo in ceos:
        df_brc_crc_mapping_ceo = utilities.filter_dataframe_column(df_brc_crc_mapping, cols.district_name, [ceo])

        deo_elems = df_brc_crc_mapping_ceo[cols.deo_name_elm].unique()
        deo_secs = df_brc_crc_mapping_ceo[cols.deo_name_sec].unique()

        ceo_deo_mapping[ceo] = {
            "Elementary_DEOs" : deo_elems.tolist(),
            "Secondary_DEOs" : deo_secs.tolist()
        }

    return ceo_deo_mapping


def get_and_save_ceo_deo_mapping():
    """
    Function to fetch the CEO to DEO mapping from BRC CRC mapping file
    and save the resulting mapping dictionary as a JSON file.
    """

    # Get the mapping
    ceo_deo_mapping = get_ceo_deo_mapping()

    # Get the path where the JSON needs to be stored
    mapping_data_dir_path = file_utilities.get_mapping_data_dir_path()
    file_path = file_utilities.get_file_path('CEO_DEO_mapping.json', mapping_data_dir_path)

    # Write the dictionary to the JSON file
    with open(file_path, 'w') as file:
        json.dump(ceo_deo_mapping, file, indent=4)



def get_no_of_elem_deos():
    """
    Function to fetch number of elementary DEOs

    Returns:
    -------
    Number of elementary DEOs
    """

    no_of_elem_deos = 0

    ceo_deo_mapping = get_ceo_deo_mapping()

    # For each ceo, get the number of elementary DEOs and update the total number
    for ceo in ceo_deo_mapping.keys():
        no_of_elem_deos += len(ceo_deo_mapping[ceo]['Elementary_DEOs'])

    return no_of_elem_deos

def get_no_of_sec_deos():
    """
    Function to fetch number of secondary DEOs

    Returns:
    -------
    Number of secondary DEOs
    """

    no_of_sec_deos = 0

    ceo_deo_mapping = get_ceo_deo_mapping()

    # For each ceo, get the number of elementary DEOs and update the total number
    for ceo in ceo_deo_mapping.keys():
        no_of_sec_deos += len(ceo_deo_mapping[ceo]['Secondary_DEOs'])

    return no_of_sec_deos



if __name__ == "__main__":
    get_and_save_ceo_deo_mapping()





