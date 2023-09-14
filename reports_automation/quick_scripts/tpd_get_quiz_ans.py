import sys
sys.path.append('../')
import pandas as pd
# To get the dataframe object as excel
#first one is User selected answers file and next is file with qstns and answers
df=pd.read_excel(r'C:\Users\TAMILL\30243.xlsx')
df1=pd.read_excel(r'C:\Users\TAMILL\30243ans.xlsx')
print(df.describe())
#joining qstn with choice to match with usa db
print(df1.head(4))
# To get qstns tex for giving heading
list = df1['Questions'].unique()
n=df1['Questions'].nunique()
df1['cstrng']=df1['q_id'].astype(str)+df1['choice_id'].astype(str)
#sort
list.sort()
print(list)
#sorting answer string
df.sort_values('AnswerString')
#splitting comma separated values
df[list] = df.AnswerString.str.split(',', expand=True)
print(df.head())
df1.drop(columns=['Questions','choice_id'],axis=1,inplace=True)
df1['cstrng']=df1[list[n]]
df2=pd.merge(df,df1,how='inner',on='list[n]')
#df1.to_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\tpd_303243_q&a.xlsx')
#df.to_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\tpd_30243_usa.xlsx')
df2.to_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\tpd_303243prac.xlsx')

