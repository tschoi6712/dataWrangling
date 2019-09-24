import csv

csvfile = open('../../data/chp3/data-text.csv', 'r')
reader = csv.reader(csvfile)                        # 매 행을 리스트

for row in reader:
    print(row)


