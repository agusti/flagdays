import calendar
import argparse
import json
from datetime import datetime

"""
@author: Agusti Pellicer
"""

#Days according to Wikipedia http://en.wikipedia.org/wiki/Flag_days_in_Finland
DAYS = {'Kalevala day' : '28/02', 'Finnish Defence Forces day' : '04/06', 'Independence day' : '06/12', 'Runerberg day' : '05/02',
        'Equality day' : '19/03', '09/04' : 'Finnish language day', 'National War Veterans\' day' : '27/04' , 'Europe day' : '09/05',
        'Finnish identity day' : '12/05', 'Eino Leino day' : '06/07', 'Finnish Literature day' : '10/10', 'United Nations day' : '24/10',
        'Swedish identity day' : '06/11', 'Finnish music day' : '08/12'}

def special_days(year):
    """ Generate the days that are dynamic """
    #Second Sunday of May is Mother's day
    #Third Sunday of May is Memorial day for the war dead
    c = calendar.monthcalendar(year, 5)
    first_week = c[0]
    second_week = c[1]
    third_week = c[2]
    fourth_week = c[3]
    if first_week[calendar.SUNDAY]:
        mother_day = str(second_week[calendar.SUNDAY]) + '/05'
        memorial_day = str(third_week[calendar.SUNDAY]) + '/05'
    else:
        mother_day = str(third_week[calendar.SUNDAY]) + '/05'
        memorial_day = str(fourth_week[calendar.SUNDAY] ) + '/05'
    #Saturday between 20 and 26 June
    c = calendar.monthcalendar(year, 6)
    third_week = c[2]
    fourth_week = c[3]
    if third_week[calendar.SATURDAY] >= 20:
        midsummer_day = str(third_week[calendar.SATURDAY]) + '/06'
    else:
        midsummer_day = str(fourth_week[calendar.SATURDAY]) + '/06'

    #Second Sunday in November is Father's day
    c = calendar.monthcalendar(year, 11)
    first_week = c[0]
    second_week = c[1]
    third_week = c[2]
    if first_week[calendar.SUNDAY]:
        father_day = str(second_week[calendar.SUNDAY]) + '/11'
    else:
        father_day = str(third_week[calendar.SUNDAY]) + '/11'
    return {'Mother\'s day' : mother_day, 'Memorial\'s day' : memorial_day, 'Midsummer day' : midsummer_day, 'Father\'s day' : father_day}

def generate_json(years, output="years.json"):
    """ Generates the JSON for the specified years """
    for year in years:
        special = special_days(year)
        DAYS.update(special)
        with open(output, 'w') as outfile:
            json.dump(DAYS, outfile)

def main():
    """ Parse the arguments and generate the json """
    parser = argparse.ArgumentParser(description='Generate JSON of the Finnish flag days for specific year(s)')
    parser.add_argument('--years', '-y', nargs='*', help='Specify the years', type=int, choices=range(1970, 2100), required=True)
    parser.add_argument('--output', '-o', nargs='?', help='Specify the output file')
    
    if not parser.parse_args().output:
        generate_json(parser.parse_args().years)
    else
        generate_json(parser.parse_args().years, parser.parse_args().output)
        
if __name__ == '__main__':
    main()