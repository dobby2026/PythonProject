"""
파일명: EX14-04-csvReader.py
"""

import csv

with open('차량관리.csv', 'r', newline='', encoding='UTF-8') as file:
    csv_reader = csv.reader(file, delimiter=',')
    for line in csv_reader:
        print(line)