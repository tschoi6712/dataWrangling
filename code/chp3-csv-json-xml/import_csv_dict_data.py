import csv

csvfile = open('../../data/chp3/data-text.csv', 'r')
reader = csv.DictReader(csvfile)                    # 매 행을 딕셔너리

for row in reader:
    print(row)

