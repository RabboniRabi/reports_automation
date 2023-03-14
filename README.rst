	
Project Introduction:
	 Python project to automate all or most of the process of generating data reports for the Department of School Education, Government of TamilNadu.

Technologies:
  Languages
    Python
  Libraries
    Pandas,
    MySql,
    XlsxWriter,
    Openpyxl,
    SQLAlchemy,
    EasyGUI.


Project Description:
  This project contains modules to help in the automated generation of reports for various domains in the administration of TN Department of School Education (Example   - Library, infrastructure, sports, attendance, observations etc.).

  The automated reports can be broadly classified  into ad hoc reports and ceo review reports.
  
  Ad hoc Reports:
    The Ad hoc reports usually generate reports with data at district level. Ad hoc reports are further classified into two types: (a) custom reports, (b) reports that     can be generated through an ad hoc report generator. The final report is aggregated and summarized at district level using JSON provided arguments and the final       output report is stored in an excel file.
  CEO Review Reports:
	  The Chief Education Officers’ (CEO) review reports are generated at (District Education Officer) DEO & block level. The reports are split into two - for DEO-           Elementary and DEO-Secondary. The generated report contains information about monitored metrics along with district, block information. The final report is also       ranked at DEO level. The ceo report generator uses values provided in a JSON configuration file to process the source data and create the report. The final output     report is stored in an excel file.
  JSON Documentation:
   	The JSON report configurations and the ceo report generator/ad hoc report generator work along with the source data to create reports. The values and the               directions needed for the generation of report at each stage is provided in the JSON configuration.
	The JSON configuration will contain information for:
	
        - Report file configuration: report name, description, source data information.
        
        - BRC-CRC Merge: Flag for custom pre-process call before merge (True) or skip (False). BRC merge join on values. Similarly for post-process.
        
        - Elementary report:  Unranked level report arguments - what type of aggregation needs to be performed on a specified set of  columns.
        
        - Ranking_args: Type of ranking to be computed along with the arguments  for the final aggregated report.
        
        - Similar configuration for the secondary_report.
        
        - Format_config - Visual formatting configuration on how the final output excel file should look like is configured.


Getting Started:
     Prerequisites:
        Python version 3.10 and above
     Installation:
      	In the folder you want the project and reports to reside, clone the project. Also, create a folder named reports. Within this reports folder, make three new           folders: generated, source_data, and mapping_data. 
	
    	To clone:
	
     	   	    git clone https://github.com/RabboniRabi/reports_automation.git
    	Install the necessary libraries using the pip command.
	
	   	   Eg: pip install pandas
    	To resolve mysql dependency, install the mysql-connector-python
	
		   pip install mysql-connector-python command
    	Choose the script you want to run.
	
    	The generated reports will be stored in the generated folder.


Contributing Members: 
	Rabboni Rabi,
	Skandaa Ramani,
	Akshaya Gunasekaran.



 
 

	
	
