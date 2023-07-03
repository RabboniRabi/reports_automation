import sys
sys.path.append("../")
import pandas as pd
import utilities.file_utilities as file_utilities
import json



"""df_list = pd.read_html("https://secc.gov.in/getSCCategoryIncomeSlabStateReport.htm/33")
df = df_list[0]
print(df)
print('type of first list object: ', type(df))
file_utilities.save_to_excel({'test_data_extraction':df}, 'test_data_extraction.xlsx', index=True)

print(df)

"""


def _save_extracted_data(data, metric):
    """
    Fuction to save the extracted data in an Excel file.
    Args:
        data: raw_data with the tehsil data
        metric:

    Returns:

    """
    # Saving the extracted data in the Excel file.
    dir_path = file_utilities.get_adw_data_dir_path()
    file_utilities.save_to_excel({metric: data}, metric + '.xlsx', index=True, dir_path=dir_path)



def tehsil_data_extraction():
    """
    Function to traverse through different District's link and extract the tehsil data.

    """
    # Reading the json file.
    file_open = open("configs/index_district_mapping.json", "r")
    config = json.load(file_open)
    district = config["district_index_mapping"]
    tehsil_links = config["tehsil_links"]

    # Loop to extract tehsil level information
    for link in tehsil_links.keys():
        # Creating an empty dataframe for storing every district's tehsil information
        data = pd.DataFrame()

        for j in district.keys():
            try:
               # Formatting the html link
                df_link = tehsil_links[link].format(j)
                # Reading the html file from the link provided in the json configuration.
                df_list = pd.read_html(df_link)
                # Converting the extracted data into a dataframe.
                df = df_list[0]
                #df = df[3:]
                df.drop(df.head(3).index, inplace=True)
               # Creating a new column District.
                df['District'] = district[j]
               # Concatenating the tehsil level data with other tehsil level data
                data = pd.concat([data, df])
            except ValueError:
            # If there is a value error, the loop goes to the next iteration.
             continue

        # Reordering columns for better readability
        columns = data.columns.to_list()
        columns = columns[-1:] + columns[:-1]
        data = data[columns]

        # Saving the extracted data
        _save_extracted_data(data, link)

        # After saving deleting the dataframe.
        del data

    # Closing the json file
    file_open.close()

def state_data_extraction():
    """
    Function to extract overall State information from HTML links.

    """
    # Reading the json file.
    file_open = open("configs/index_district_mapping.json", "r")
    config = json.load(file_open)
    overall_state = config['state_links']

    for link in overall_state.keys():
        # Reading the html file from the link provided in the json configuration.
        df_list = pd.read_html(overall_state[link])
        # Converting the extracted data into a dataframe.
        df = df_list[0]
        # Saving the extracted data
        _save_extracted_data(df, link)
        # After saving deleting the dataframe.
        del df

    # Closing the json file
    file_open.close()


def main():
    """
    Internal function to call the other two functions


    """
    # For testing
    state_data_extraction()
    tehsil_data_extraction()











