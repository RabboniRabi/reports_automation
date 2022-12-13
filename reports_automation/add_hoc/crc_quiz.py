import pandas as pd
import numpy as np


data = pd.read_excel(r'C:\Users\Admin\Downloads\crc_quiz.xlsx', sheet_name='quiz')


training_data = pd.concat([pd.Series(row['teacher_id'],row['AnswerString'].split(','))
           for _, row in data.iterrows()]).reset_index()

training = pd.ExcelWriter(r'C:\Users\Admin\Downloads\crc_quiz_2.xlsx')
training_data.to_excel(training, sheet_name='Main View', index=False)

training.save()


