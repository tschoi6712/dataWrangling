from xml.etree import ElementTree as ET

tree = ET.parse('../../data/chp3/data-text.xml')
root = tree.getroot()
#print(root)
#print(dir(root))
#print(list(root))

data = root.find('Data')
#print(list(data))

'''
for observation in data:
    for item in observation:
        print(item)

for observation in data:
    for item in observation:
        print(item.text)

print(list(item))

for observation in data:
    for item in observation:
        print(item.attrib)
'''

all_data = []

for observation in data:
    record = {}
    for item in observation:

        lookup_key = list(item.attrib.keys())[0]

        if lookup_key == 'Numeric':
            rec_key = 'NUMERIC'
            rec_value = item.attrib['Numeric']
        else:
            rec_key = item.attrib[lookup_key]
            rec_value = item.attrib['Code']

        record[rec_key] = rec_value
    all_data.append(record)

print(all_data)
