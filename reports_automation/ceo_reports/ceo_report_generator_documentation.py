"""
========================================================================================================================
Module with functions will be the master code that will run the CEO reports in blocks/functions of code.
This will entail 2 main functions:
    1. Run all the code and generator all the reports in one go: generate_all():

    generate_all():
        active_configs = config_reader.get_Active_configs()
        for each active config
            ceo_raw_data = get_ceo_report_raw_data(config[code], 'raw data with brc-crc mapping', save_source=True)
            elementary_report = get_ceo_report(config[code], 'Elementary', 'ranked')
            secondary_report = get_ceo_report(config[code], 'Secondary', 'ranked')
            report_format_utilities.format_ceo_review_report(elementary_report)
            report_format_utilities.format_ceo_review_report(secondary_report)

    def get_ceo_report_raw_data(code, temp, param, save_source = False):
        config = config_reader.get_config(code)
        source_config = config['source_config']
        raw_data = data_fetcher.get_data_from_config(source_config)

a source config - > there are 2 options in the json -> if query name except OSerror -> excel file name -> except error in input



    2. Generate Generate specific reports by calling a specific definition:

    for public use:
    ===============

        A. get_ceo_report_raw_data(report_code,raw_data_level):
            [file path: reports > ceo_report_generator.py]
        ---------------------------------------------------------
            Available raw_data_level-
                1. raw data: get_data(code)
                [file path:reports > data_fetcher.py ]
                2. processed data: pre_processing_data_before_brc_merge()
                3. raw data with brc-crc mapping:  post_processing_data_after_brc_merge()

        B. get_ceo_report(report_code,report_type,report_level):
            (file path: reports > ceo_report_generator.py)
        ----------------------------------------------------------
            Available report_type-
                    (i) elementary
                    (ii) secondary

            Available raw_data_level-
                4. unranked: unranked_elementary_report()/unranked_secondary_report()
                5. ranked: ranked_elementary_report()/ranked_secondary_report()

    for internal use:
    =================
                6. format_save_elementary_report()/format_save_secondary_report()
                7. consolidate_and_index_report()

------------------------------------------------------------------------------------------------------------------------
Requirements apart from the functions:
    1. Report wise dictionary:
        This dictionary would have the list of all the reports, and the various calculations required for processing.
        These will be stored as the components required for each block/function.
    2. JSON structure for reporting:
        The JSON would store all report specific information. These would include the
        a. Code of the report
        b. Ranking Arguments (Sorting, Numerator, Denominator, Name of the metric, Ranking Value etc.)
        c. Input to decide whether or not to running the particular report
    3. Report Index Master:
        This would be a document that is available in both the elementary and secondary folders in the report_generated
        folder. It would be the updated list of reports and their corresponding report codes. This document will merge
        the final elementary and secondary reports generated, and hyperlink the individual reports to the Index sheet.
------------------------------------------------------------------------------------------------------------------------
Ripple Effects:
    1. The ranking master would get updated each time a report is generated. This will happen only when the generate_all
    function is run. As this would affect the rankings for each month, and must reflect the rank that was provided in
    the actual report shared.

========================================================================================================================
The module will work as blocks as mentioned above. The following is the list of blocks/functions that will collectively
arrive at the CEO Review Reports in a single file:

1. get_data_from_config(source_config_dict, save_source=False):
    Function:
        This function would get the raw data from either the database or an excel file.
        If the query does not run, it would expect an excel file, all of the raw data will be saved in a folder.
        A specific code and source file information will be stored as dictionary.
        For example: If the students ageing in common pool report is requested, the code will be CP in the dictionary.

        When generate_ceo_report is called:
        get_source_data will run only for the specific code mentioned in the function. To continue the example above,
        only the raw data for the common pool report report will be generated.

        When generate_all is called,
        get_source_data will run sequentially across the whole list as a loop, completing each report one by one.

        Parameters:

    Returns:
        A dataframe object(df) with the raw data for each report without any processing (depending on which of the 2
        main functions are called).
------------------------------------------------------------------------------------------------------------------------
2. pre_processing_data_before_brc_merge():
    Function:
        Using the df returned by get_source_data(), this function would ensure that the raw data is crunched down to a
        school level (using UDISE Code as the primary key). This would vary depending on level of the source data.

        Parameters:

    Returns:
        The final df that will be used before mapping with the master BRC-CRC file.
------------------------------------------------------------------------------------------------------------------------
3. map_data_with_brc(pre_processed_data, merge_dict):
    Function:
        This function maps the raw data with BRC CRC mapping. The join is done on school the UDISE Code.

        Parameters:
        raw_data: Pandas DataFrame
            The raw data to be updated with brc-crc mapping.
        merge_dict: dict
            A merge param - merge param value key-value pair to be used to specify the type of merging
                Eg: merge_dict = {
                    'on_values' : ['district', 'block','school_name', 'school_category', 'udise_col'],
                    'how' : 'outer'
                        }

    Returns:
        The mapped df updated with BRC-CRC mapping at a school level.


------------------------------------------------------------------------------------------------------------------------
4. post_processing_data_after_brc_merge():
    Function:
        This function uses the mapped raw data and processes it further to bring to the required format before splitting
        it up into elementary or secondary reports.

        Parameters:

    Returns:
        The final processed data required before splitting the data up into elementary and secondary reports.
========================================================================================================================
5.a.(i). unranked_elementary_report():
   Function:
        This function uses the processed data and prepares the elementary report up to the ranking step.

        Parameters:

    Returns:
        The final elementary data that will be used for ranking the reports.
------------------------------------------------------------------------------------------------------------------------
5.a.(ii). ranked_elementary_report():
   Function:
       This function ranks the elementary report, whilst updating the ranking master as well.

        Parameters:

    Returns:
        The final elementary report that will be printed, and ready for formatting.
------------------------------------------------------------------------------------------------------------------------
5.b.(i). unranked_for_secondary_report():
   Function:
        This function uses the processed data and prepares the secondary report up to the ranking step.

        Parameters:

    Returns:
        The final secondary data that will be used for ranking the reports.
------------------------------------------------------------------------------------------------------------------------
5.b.(ii). ranked_secondary_report():
   Function:
       This function ranks the secondary report, whilst updating the ranking master as well.

        Parameters:

    Returns:
        The final secondary report that will be printed, and ready for formatting.
------------------------------------------------------------------------------------------------------------------------
6.a. format_save_elementary_report():
    Function:
        This function performs the following formatting actions specific to the elementary report:
        (i) Outlines
        (ii) Adding back ranks
        (iii) Font formatting
        (iv) Merging the top row for the heading
        (v) Adding a row for the column index

        Parameters:

    Returns:
        This is the report that will be saved into the elementary reports folder.
------------------------------------------------------------------------------------------------------------------------
6.b. format_save_secondary_report():
    Function:
        This function performs the following formatting actions specific to the secondary report:
        (i) Outlines
        (ii) Adding back ranks
        (iii) Font formatting
        (iv) Merging the top row for the heading
        (v) Adding a row for the column index

        Parameters:

    Returns:
        This is the report that will be saved into the secondary reports folder.
------------------------------------------------------------------------------------------------------------------------
7. consolidate_and_index_report():
        Function:
            This function will merge all the individual reports in the elementary and secondary report folders separately
            and index them in their respective files.

            Parameters:

        Returns:
            The 2 final CEO Review Reports that will be extracted as excel files.
========================================================================================================================
"""