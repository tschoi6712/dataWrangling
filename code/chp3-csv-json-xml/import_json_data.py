import json

json_data = open('../../data/chp3/data-text.json').read()

data = json.loads(json_data)

for item in data:
    print(item)

# csv.reader('열린 파일'), json.loads('문자열')
filename = 'data-text.json'
type(open(filename, 'r'))
type(open(filename).read())
