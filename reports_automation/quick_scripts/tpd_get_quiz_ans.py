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
print(n)
df1['cstrng']=df1['q_id'].astype(str)+df1['choice_id'].astype(str)
#sort
list.sort()
print(list)
#sorting answer string
df.sort_values('AnswerString')
#splitting comma separated values
df[list] = df.AnswerString.str.split(',', expand=True)
#df.drop(columns=['Questions'],axis=1,inplace=True)
print(df.head())
df1.drop(columns=['Questions','choice_id','q_id'],axis=1,inplace=True)
s=[0,1,2,3,4]
for q in range(n):
  i=list[q]
  l=i+"ans"
  k=i+"choice"
  print(i)
  df1.rename(columns={df1.columns[2]:i},inplace=True)
  df1.rename(columns={df1.columns[1]:k},inplace=True)
  df1.rename(columns={df1.columns[0]:l},inplace=True)
  df2=pd.merge(df,df1,how='inner',on=i)
#df1.to_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\tpd_3032_43_q&a.xlsx')
#df.to_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\tpd_30243_usa.xlsx')
  df2.to_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\tpd_30324_3prac.xlsx')

