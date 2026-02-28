import os


#main
def add_file(year, month):
    print(f'C:\Money Mentor\data{year}\{month}')
    os.makedirs(f'C:\Money Mentor\data\{year}\{month}')

add_file(2026, 'Febuary')