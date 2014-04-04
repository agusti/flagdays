import calendar
import argparse
import json
from datetime import datetime

"""
@author: Agusti Pellicer
"""

#Days according to Wikipedia http://en.wikipedia.org/wiki/Flag_days_in_Finland
DAYS = [{'description' : 'Kalevala day', 'date' : '28/02'},
        {'description' : 'Finnish Defence Forces day', 'date' : '04/06'}, 
        {'description' : 'Independence day', 'date' : '06/12'}, 
        {'description' : 'Runerberg day', 'date' : '05/02'},
        {'description' : 'Equality day', 'date' : '19/03'}, 
        {'description' : 'Finnish language day', 'date' : '09/04'}, 
        {'description' : 'National War Veterans\' day', 'date' : '27/04'}, 
        {'description' : 'Europe day', 'date' : '09/05'},
        {'description' : 'Finnish identity day', 'date' : '12/05'}, 
        {'description' : 'Eino Leino day', 'date' : '06/07'}, 
        {'description' : 'Finnish Literature day', 'date' : '10/10'}, 
        {'description' : 'United Nations day', 'date' : '24/10'},
        {'description' : 'Swedish identity day', 'date' : '06/11'}, 
        {'description' : 'Finnish music day', 'date' : '08/12'}]

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
    #Return the special days
    return [{'description' : 'Mother\'s day', 'date' : mother_day},
            {'desctiption' : 'Memorial\'s day', 'date' : memorial_day},
            {'description' : 'Midsummer day', 'date' : midsummer_day},
            {'description' : 'Father\'s day', 'date' : father_day}]

def generate_json(years, output="years.json"):
    """ Generates the JSON for the specified years """
    days = [{str(year):DAYS + special_days(year) for year in years}]
    with open(output, 'w') as outfile:
        json.dump(days[0], outfile)

def main():
    """ Parse the arguments and generate the json """
    parser = argparse.ArgumentParser(description='Generate JSON of the Finnish flag days for specific year(s)')
    parser.add_argument('--years', '-y', nargs='*', help='Specify the years', type=int, choices=range(1970, 2100), required=True)
    parser.add_argument('--output', '-o', nargs='?', help='Specify the output file')
    
    if not parser.parse_args().output:
        generate_json(parser.parse_args().years)
    else:
        generate_json(parser.parse_args().years, parser.parse_args().output)
        
if __name__ == '__main__':
    main()