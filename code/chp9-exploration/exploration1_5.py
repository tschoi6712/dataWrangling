"""
Part 1 / 5

Note: this is an IPython session walking through the beginning of Chapter 9 to import the
data into `agate`. It's used as an example of stepping through ideas as you work with your
data in iPython. It was saved using iPython %history -f importing_data.py so
you can use it in the repository. Obviously, if you'd like to reuse bits of this
code, it should be rewritten as a proper script :) -- @kjam
"""

import xlrd
import agate


workbook = xlrd.open_workbook('../../data/unicef/unicef_oct_2014.xls')
print(workbook.nsheets)
print(workbook.sheet_names())

sheet = workbook.sheets()[0]
print(sheet.nrows)
print(sheet.row_values(0))

for r in range(sheet.nrows):
    print(r, sheet.row(r))

title_rows = zip(sheet.row_values(4), sheet.row_values(5))
print(title_rows)

titles = [t[0] + ' ' + t[1] for t in title_rows]
titles = [t.strip() for t in titles]
print(titles)

country_rows = [sheet.row_values(r) for r in range(6, 114)]
print(country_rows)



from xlrd.sheet import ctype_text
import agate

text_type = agate.Text()
number_type = agate.Number()
boolean_type = agate.Boolean()
date_type = agate.Date()

example_row = sheet.row(6)
print(example_row)
print(example_row[0].ctype)
print(example_row[0].value)
print(ctype_text)


types = []

for v in example_row:
    value_type = ctype_text[v.ctype]
    if value_type == 'text':
        types.append(text_type)
    elif value_type == 'number':
        types.append(number_type)
    elif value_type == 'xldate':
        types.append(date_type)
    else:
        types.append(text_type)

print(types)
print(titles)

table = agate.Table(country_rows, titles, types)


def remove_bad_chars(val):
    if val == '-':
        return None
    return val

cleaned_rows = []
for row in country_rows:
    cleaned_row = [remove_bad_chars(rv) for rv in row]
    cleaned_rows.append(cleaned_row)

table = agate.Table(cleaned_rows, titles, types)
print(table)


def get_new_array(old_array, function_to_clean):
    new_arr = []
    for row in old_array:
        cleaned_row = [function_to_clean(rv) for rv in row]
        new_arr.append(cleaned_row)
    return new_arr

cleaned_rows = get_new_array(country_rows, remove_bad_chars)

table = agate.Table(cleaned_rows, titles, types)
table.print_table(max_columns=7)
print(table.column_names)


"""
Part 2 / 5

NOTE: this is a continuation of the IPython session beginning with importing_data.py.
It explores the table using some agate methods. Again, it is here as an example,
not as a usable script :) --@kjam
"""


most_egregious = table.order_by('Total (%)', reverse=True).limit(10)
for r in most_egregious.rows:
    print(r)

most_females = table.order_by('Female', reverse=True).limit(10)
for r in most_females.rows:
    print('{}: {}%'.format(r['Countries and areas'], r['Female']))

female_data = table.where(lambda r: r['Female'] is not None)
most_females = female_data.order_by('Female', reverse=True).limit(10)
for r in most_females.rows:
    print('{}: {}%'.format(r['Countries and areas'], r['Female']))


(lambda x: 'Positive' if x >= 1 else 'Zero or Negative')(0)
(lambda x: 'Positive' if x >= 1 else 'Zero or Negative')(4)


table.columns['Place of residence (%) Urban'].aggregate(agate.Mean())
col = table.columns['Place of residence (%) Urban']
table.aggregate(agate.Mean('Place of residence (%) Urban'))


has_por = table.where(lambda r: r['Place of residence (%) Urban'] is not None)
has_por.aggregate(agate.Mean('Place of residence (%) Urban'))

first_match = has_por.find(lambda x: x['Rural'] > 50)
print(first_match['Countries and areas'])


ranked = table.compute([('Total Child Labor Rank', agate.Rank('Total (%)', reverse=True)),])

for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
    print(row['Total (%)'], row['Total Child Labor Rank'])


def reverse_percent(row):
    return 100 - row['Total (%)']

ranked = table.compute([('Children not working (%)', agate.Formula(number_type, reverse_percent)), ])

ranked = ranked.compute([('Total Child Labor Rank', agate.Rank('Children not working (%)')), ])

for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
    print(row['Total (%)'], row['Total Child Labor Rank'])



"""
Part 3 / 5

NOTE: This is continued iPython exploration joining the child labor data
with corruption perception data. It also begins to explore some of the powerful
`agate` library features for statistical correlations. Again, this is not
to be used as a script, only an example of the exploration covered in
Chapter 9. --@kjam
"""
import agate
import xlrd

from xlrd.sheet import ctype_text

text_type = agate.Text()
number_type = agate.Number()
boolean_type = agate.Boolean()
date_type = agate.Date()


def remove_bad_chars(val):
    if val == '-':
        return None
    return val


def get_types(example_row):
    types = []
    for v in example_row:
        value_type = ctype_text[v.ctype]
        if value_type == 'text':
            types.append(text_type)
        elif value_type == 'number':
            types.append(number_type)
        elif value_type == 'xldate':
            types.append(date_type)
        else:
            types.append(text_type)
    return types


workbook = xlrd.open_workbook('../../data/unicef/unicef_oct_2014.xls')
sheet = workbook.sheets()[0]

title_rows = zip(sheet.row_values(4), sheet.row_values(5))
titles = [t[0] + ' ' + t[1] for t in title_rows]
titles = [t.strip() for t in titles]

country_rows = [sheet.row_values(r) for r in range(6, 114)]
cleaned_rows = []

for row in country_rows:
    cleaned_row = [remove_bad_chars(rv) for rv in row]
    cleaned_rows.append(cleaned_row)

example_row = sheet.row(6)
types = get_types(example_row)

table = agate.Table(cleaned_rows, titles, types)
ranked = table.compute([('Total Child Labor Rank',
                         agate.Rank('Total (%)', reverse=True)), ])


cpi_workbook = xlrd.open_workbook(
    '../../data/chp9/corruption_perception_index.xls')
cpi_sheet = cpi_workbook.sheets()[0]

for r in range(cpi_sheet.nrows):
    print(r, cpi_sheet.row_values(r))

cpi_title_rows = zip(cpi_sheet.row_values(1), cpi_sheet.row_values(2))
cpi_titles = [t[0] + ' ' + t[1] for t in cpi_title_rows]
cpi_titles = [t.strip() for t in cpi_titles]
cpi_rows = [cpi_sheet.row_values(r) for r in range(3, cpi_sheet.nrows)]


def get_table(new_arr, types, titles):
    try:
        table = agate.Table(new_arr, titles, types)
        return table
    except Exception as e:
        print(e)

cpi_types = get_types(cpi_sheet.row(3))
cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)

print(cpi_titles)

cpi_titles[0] = cpi_titles[0] + ' Duplicate'
cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)

cpi_and_cl = cpi_table.join(ranked, 'Country / Territory',
                            'Countries and areas', inner=True)

cpi_and_cl.print_table()
cpi_and_cl.column_names
len(cpi_and_cl.rows)
len(cpi_table.rows)
len(ranked.rows)

for r in cpi_and_cl.order_by('CPI 2013 Score').limit(10).rows:
    print('{}: {} - {}%'.format(r['Country / Territory'],
                                r['CPI 2013 Score'], r['Total (%)']))

import numpy

#numpy.corrcoef(cpi_and_cl.columns['Total (%)'].values(), cpi_and_cl.columns['CPI 2013 Score'].values())[0, 1]


np_cor = numpy.corrcoef(
    [float(t) for t in cpi_and_cl.columns['Total (%)'].values()],
    [float(s) for s in cpi_and_cl.columns['CPI 2013 Score'].values()])[0, 1]

print(np_cor)


import agatestats
agatestats.patch()

std_dev_outliers = cpi_and_cl.stdev_outliers('Total (%)', deviations=3, reject=False)
len(std_dev_outliers.rows)

std_dev_outliers = cpi_and_cl.stdev_outliers('Total (%)', deviations=5, reject=False)
len(std_dev_outliers.rows)


mad = cpi_and_cl.mad_outliers('Total (%)')
for r in mad.rows:
    print(r['Country / Territory'], r['Total (%)'])



"""
Part 4 / 5
NOTE: This is a continuation of the IPython session working with
child labor and corruption indexes to determine correlation. Again, it
should not be used as a script, but instead an example of functions and
methods when exploring data.
"""
import json
import agate

country_json = json.loads(open('../../data/chp9/earth.json', 'r', encoding='UTF8').read())
country_dict = {}

for dct in country_json:
    country_dict[dct['name']] = dct['parent']


def get_country(country_row):
    return country_dict.get(country_row['Country / Territory'].lower())

cpi_and_cl = cpi_and_cl.compute([('continent',
                                  agate.Formula(text_type, get_country)), ])
print(cpi_and_cl.column_names)

for r in cpi_and_cl.rows:
    print(r['Country / Territory'], r['continent'])

no_continent = cpi_and_cl.where(lambda x: x['continent'] is None)
for r in no_continent.rows:
    print(r['Country / Territory'])

cpi_and_cl = cpi_table.join(ranked, 'Country / Territory',
                            'Countries and areas', inner=True)
country_json = json.loads(open(
    '../../data/chp9/earth-cleaned.json', 'r', encoding='UTF8').read())

for dct in country_json:
    country_dict[dct['name']] = dct['parent']

cpi_and_cl = cpi_and_cl.compute([('continent',
                                  agate.Formula(text_type, get_country)), ])

for r in cpi_and_cl.rows:
    print(r['Country / Territory'], r['continent'])

grp_by_cont = cpi_and_cl.group_by('continent')
print(grp_by_cont)

for cont, table in grp_by_cont.items():
    print(cont, len(table.rows))

agg = grp_by_cont.aggregate([('cl_mean', agate.Mean('Total (%)')),
                             ('cl_max', agate.Max('Total (%)')),
                             ('cpi_median', agate.Median('CPI 2013 Score')),
                             ('cpi_min', agate.Min('CPI 2013 Score'))])

print(agg)

print(agg.print_table())

print(agg.print_bars('continent', 'cl_max'))




"""
Part 5 / 5 (TBC in Chapter 10 with some charts)
NOTE: This is the final parts of Chapter 9's data exploration
using `agate`. This is just to be used as an example of how to
explore and investigate data. This section focuses on the dataset
from Africa and investigating correlation and potential case studies.
"""


africa_cpi_cl = cpi_and_cl.where(lambda x: x['continent'] == 'africa')

for r in africa_cpi_cl.order_by('Total (%)', reverse=True).rows:
    print("{}: {}% - {}".format(r['Country / Territory'], r['Total (%)'],
            r['CPI 2013 Score']))

import numpy

print(numpy.corrcoef(
    [float(t) for t in africa_cpi_cl.columns['Total (%)'].values()],
    [float(c) for c in africa_cpi_cl.columns['CPI 2013 Score'].values()])[0, 1])

africa_cpi_cl = africa_cpi_cl.compute([('Africa Child Labor Rank', agate.Rank('Total (%)', reverse=True)), ])
africa_cpi_cl = africa_cpi_cl.compute([('Africa CPI Rank',
                                          agate.Rank('CPI 2013 Score')),
                                        ])
africa_cpi_cl.print_table()

cpi_mean = africa_cpi_cl.aggregate(agate.Mean('CPI 2013 Score'))
cl_mean = africa_cpi_cl.aggregate(agate.Mean('Total (%)'))

print(cl_mean)
print(cpi_mean)

def highest_rates(row):
    if row['Total (%)'] > cl_mean and row['CPI 2013 Score'] < cpi_mean:
        return True
    return False

highest_cpi_cl = africa_cpi_cl.where(lambda x: highest_rates(x))

for r in highest_cpi_cl.rows:
    print("{}: {}% - {}".format(r['Country / Territory'], r['Total (%)'],
        r['CPI 2013 Score']))

