import sys
sys.path.append('../')

import utilities.utilities as utilities
import pandas as pd

# Global variables
district = 'District'
ed_district = 'Edu.Dist'
block = 'Block'
total_schls_not_started = 'Total Schools Not Started'

# Read the excel report as a Pandas DataFrame object
df_report = pd.read_excel(r'/home/rabboni/Downloads/Student-health-checkup-rpt.xlsx', sheet_name='Report',skiprows=4)


# Group the data down to block level (collapsing schools), counting total students, students screened, not screened
df_block_level = df_report.groupby([district, ed_district, block],sort=False)[['Total','Screened', 'UnScreened']].sum().reset_index()


# Get a dataframe of schools where no child has been screened
df_not_screened = df_report[df_report['Screened'] == 0]

# Get a dataframe with block wise count of schools that have not started screening
df_not_started = df_not_screened.groupby([district, ed_district, block])[['School']].count().reset_index()
df_not_started.rename(columns = {'School': total_schls_not_started}, inplace = True)


# Group to block level, counting number of schools in each block
df_schools_count = df_report.groupby([district, ed_district, block])[['School']].count().reset_index()
df_schools_count.rename(columns = {'School':'Total Schools'}, inplace = True)

# Create a block level overview of total students, number of schools and number of schools not started screening
df_overview = df_block_level.merge(df_not_started[[district, ed_district, block, total_schls_not_started]])

df_overview = df_overview.merge(df_schools_count[[district, ed_district, block, 'Total Schools']])

# Add a % students screened   column to the overview dataframe
df_overview['% Students Screened'] = df_overview['Screened']/df_overview['Total']

# Add a column for number of schools that have started screening at each block
df_overview['Total Schools Started'] = df_overview['Total Schools'] - df_overview[total_schls_not_started]

# Add a % of schools not started screening
df_overview['% Schools Not Started'] = df_overview[total_schls_not_started]/df_overview['Total Schools']
# Convert to % format upto two decimal places
df_overview.loc[:, "% Schools Not Started"] = df_overview["% Schools Not Started"].map('{:.2%}'.format)

# Rank blocks based on % schools not started values
df_overview['Rank'] = df_overview['% Schools Not Started'].rank(method='min',ascending=True)


# Ranking for Educational District
ed_rank = df_overview.groupby([ed_district])[[total_schls_not_started, 'Total Schools']].sum()
ed_rank['EDist_Data'] = (ed_rank[total_schls_not_started]/ed_rank['Total Schools'])
ed_rank['EDist_Rank'] = ed_rank['EDist_Data'].rank(method='min',ascending=True)
ed_rank = ed_rank.reset_index()

# Populate educational district ranks calculated above in a new column in the df_overview dataframe
df_overview['ERank'] = df_overview[ed_district]. apply(utilities.xlookup, args=(ed_rank[ed_district], ed_rank['EDist_Rank']))

# Ranking for District
d_rank = df_overview.groupby(['District'])[[total_schls_not_started, 'Total Schools']].sum()
d_rank['Dist_Data'] = (d_rank[total_schls_not_started]/d_rank['Total Schools'])
d_rank['Dist_Rank'] = d_rank['Dist_Data'].rank(method='min',ascending=True)
d_rank = d_rank.reset_index()

# Populate district ranks calculated above in a new column in the df_overview dataframe
df_overview['DRank'] = df_overview[district]. apply(utilities.xlookup, args=(d_rank[district], d_rank['Dist_Rank']))

# Sorting the data post application of ranks
df_overview = df_overview.sort_values(['DRank', district, 'ERank', ed_district, 'Rank'],
                      ascending=[True, True, True, True, True])

print ('df_overview:', df_overview)                      


# Creating View for "c1_total  2021 View" for Edu Dist
TV_ED = pd.DataFrame(df_overview[ed_district])

"""
TV_ED['ERank'] = TV_ED['Edu.Dist']. apply(xlookup, args=(ed_rank['Edu.Dist'], ed_rank['EDist_Rank']))

TV_ED['ERank1'] = TV_ED['Edu.Dist']. apply(xlookup, args=(ed_rank['Edu.Dist'], ed_rank['Edu.Dist']))

TV_ED['ERank1'] = TV_ED['ERank1'] + ' Total'

TV_ED = TV_ED.drop_duplicates(keep='first')

# Creating View for "c1_total  2021 View" for Dist

TV_D = pd.DataFrame(df4['District'])

TV_D['DRank'] = TV_D['District']. apply(xlookup, args=(d_rank['District'], d_rank['Dist_Rank']))

TV_D['DRank1'] = TV_D['District']. apply(xlookup, args=(d_rank['District'], d_rank['District']))

TV_D['DRank1'] = TV_D['DRank1'] + ' Total'

TV_D = TV_D.drop_duplicates(keep='first')

# Remove last 2 columns of df4 before printing
df4.drop(columns=df4.columns[-2:],
        axis=1,
        inplace=True)


df4 =df4[['District', 'Edu.Dist', 'Block','Total','Screened', 'Unscreened','% Students Screened', 'Total Schools', 'Total Schools Started',
          'Total Schools Not Started','% Schools Not Started','Rank' ]]


# Final DataFrame
df_1 = pd.DataFrame(df4)

datatoexcel = pd.ExcelWriter(r'/home/rabboni/Downloads/health.xlsx')

# write DataFrame to excel
df_1.to_excel(datatoexcel, sheet_name='Main View', index=False)

# save the excel
datatoexcel.save()"""


