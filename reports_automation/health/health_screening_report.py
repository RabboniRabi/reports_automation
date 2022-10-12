import pandas as pd

df1 = pd.read_excel(r'/home/rabboni/Downloads/Student-health-checkup-rpt.xlsx', sheet_name='Report',skiprows=4)


# Sum of All students in DataFrame2

df2 = df1.groupby(['District', 'Edu.Dist', 'Block'])[['Total','Screened', 'Unscreened']].sum().reset_index()

df3 = df1[df1['Screened'] == 0]

df4a = df3.groupby(['District', 'Edu.Dist', 'Block'])[['School']].count().reset_index()
df4a.rename(columns = {'School': 'Total Schools Not Started'}, inplace = True)

df6 = df1.groupby(['District', 'Edu.Dist', 'Block'])[['School']].count().reset_index()
df6.rename(columns = {'School':'Total Schools'}, inplace = True)

df4 = df2.merge(df4a[['District', 'Edu.Dist', 'Block', 'Total Schools Not Started']])

df4 = df4.merge(df6[['District', 'Edu.Dist', 'Block', 'Total Schools']])

df4['% Students Screened'] = df4['Screened']/df4['Total']

df4['Total Schools Started'] = df4['Total Schools'] - df4['Total Schools Not Started']

df4['% Schools Not Started'] = df4['Total Schools Not Started']/df4['Total Schools']


# Ranking for Block
df4['Rank'] = df4['% Schools Not Started'].rank(method='min',ascending=True)

# Ranking for Educational District
ed_rank = df4.groupby(['Edu.Dist'])[['Total Schools Not Started', 'Total Schools']].sum()
ed_rank['EDist_Data'] = (ed_rank['Total Schools Not Started']/ed_rank['Total Schools'])
ed_rank['EDist_Rank'] = ed_rank['EDist_Data'].rank(method='min',ascending=True)
ed_rank = ed_rank.reset_index()

# Ranking for District
d_rank = df4.groupby(['District'])[['Total Schools Not Started', 'Total Schools']].sum()
d_rank['Dist_Data'] = (d_rank['Total Schools Not Started']/d_rank['Total Schools'])
d_rank['Dist_Rank'] = d_rank['Dist_Data'].rank(method='min',ascending=True)
d_rank = d_rank.reset_index()

# Vlookup for Ed_District
def xlookup(lookup_value, lookup_array, return_array, if_not_found: str = ''):
    match_value = return_array.loc[lookup_array == lookup_value]
    if match_value.empty:
        return 0 if if_not_found == '' else if_not_found

    else:
        return match_value.tolist()[0]


df4['ERank'] = df4['Edu.Dist']. apply(xlookup, args=(ed_rank['Edu.Dist'], ed_rank['EDist_Rank']))

# Vlookup for District Rank


df4['DRank'] = df4['District']. apply(xlookup, args=(d_rank['District'], d_rank['Dist_Rank']))

# Changing % format
df4.loc[:, "% Schools Not Started"] = df4["% Schools Not Started"].map('{:.2%}'.format)

# Sorting df4
df4 = df4.sort_values(['DRank', 'District', 'ERank', 'Edu.Dist', 'Rank'],
                      ascending=[True, True, True, True, True])


# Creating View for "c1_total  2021 View" for Edu Dist
TV_ED = pd.DataFrame(df4['Edu.Dist'])

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
datatoexcel.save()


