import sys
sys.path.append('../')

import utilities.dbutilities as dbutilities
import utilities.file_utilities as file_utilities
import pandas as pd

day1 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-09-15.xlsx',sheet_name= 'Summary')
print(day1)
day2 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-09-18.xlsx',sheet_name= 'Summary')
print(day2)
day3 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-09-19.xlsx',sheet_name= 'Summary')
print(day2)
day4 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-09-20.xlsx',sheet_name= 'Summary')
day5 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-09-21.xlsx',sheet_name= 'Summary')
day6 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-09-22.xlsx',sheet_name= 'Summary')
day7 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-09-25.xlsx',sheet_name= 'Summary')
day8 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-09-26.xlsx',sheet_name= 'Summary')
print(day8)
day9 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-09-27.xlsx',sheet_name= 'Summary')
day10 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-10-03.xlsx',sheet_name= 'Summary')
day11 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-10-04.xlsx',sheet_name= 'Summary')
day12 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-10-05.xlsx',sheet_name= 'Summary')
day13 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-10-06.xlsx',sheet_name= 'Summary')
print(day9)
day14 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-10-09.xlsx',sheet_name= 'Summary')
day15 = pd.read_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\Stu_attendance_avg/Student-Marked-Attendance_2023-10-10.xlsx',sheet_name= 'Summary')
print(day15)

all_days_list = [day1,day2,day3,day4,day5,day6,day7,day8,day9,day10,day11,day12,day13,day14,day15]
all_day_df = pd.concat(all_days_list)
all_day_df.to_excel(r'C:\Users\TAMILL\Desktop\TEA\Sample\student_attendance.xlsx')
