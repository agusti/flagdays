import calendar
import argparse
import json
import datetime
import time
import copy

"""
@author: Agusti Pellicer
"""

#Days according to Wikipedia http://en.wikipedia.org/wiki/Flag_days_in_Finland
DAYS = [{'description' : 'Day of Kalevala', 'date' : '28/02', 'link': 'http://en.wikipedia.org/wiki/Kalevala'},
        {'description' : 'Day of the Finnish Defence Forces', 'date' : '04/06', 'link':'http://en.wikipedia.org/wiki/Finnish_Defence_Forces'}, 
        {'description' : 'Independence Day', 'date' : '06/12' , 'link' : 'http://en.wikipedia.org/wiki/Independence_Day_of_Finland'}, 
        {'description' : 'Birthday of the National poet Johan Ludvig Runeberg', 'date' : '05/02', 'link':'http://en.wikipedia.org/wiki/Johan_Ludvig_Runeberg'},
        {'description' : 'Day of Equality', 'date' : '19/03', 'link' : 'http://en.wikipedia.org/wiki/Minna_Canth'}, 
        {'description' : 'Day of the Finnish language', 'date' : '09/04', 'link' : 'http://en.wikipedia.org/wiki/Finnish_language'}, 
        {'description' : 'National War Veterans\' Day', 'date' : '27/04', 'link' : ''},
        {'description' : 'Vappu, the Day of Finnish Labour' , 'date' : '01/05', 'link' : 'http://en.wikipedia.org/wiki/Labour_Day'},
        {'description' : 'Europe Day', 'date' : '09/05', 'link':'http://en.wikipedia.org/wiki/Europe_Day'},
        {'description' : 'Finnish identity Day', 'date' : '12/05', 'link' : 'http://en.wikipedia.org/wiki/Johan_Vilhelm_Snellman'}, 
        {'description' : 'Eino Leino Day', 'date' : '06/07', 'link' : 'http://en.wikipedia.org/wiki/Eino_Leino'}, 
        {'description' : 'Day of Finnish literature', 'date' : '10/10', 'link' : 'http://en.wikipedia.org/wiki/Aleksis_Kivi'}, 
        {'description' : 'Day of the United Nations', 'date' : '24/10', 'link': 'http://en.wikipedia.org/wiki/United_Nations'},
        {'description' : 'Day of the Swedish Identity', 'date' : '06/11', 'link' : 'http://en.wikipedia.org/wiki/Finland-Swedish'}, 
        {'description' : 'Day of Finnish music', 'date' : '08/12', 'link': 'http://en.wikipedia.org/wiki/Jean_Sibelius'}]

def convert_date_to_js(str_date,year):
    date_s = str_date.split('/')
    d = datetime.date(year, int(date_s[1]), int(date_s[0]))
    return int(time.mktime(d.timetuple())) * 1000

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
    return [{'description' : 'Mother\'s day', 'date' : mother_day, 'link': 'http://en.wikipedia.org/wiki/Mother%27s_Day'},
            {'desctiption' : 'Memorial\'s day', 'date' : memorial_day, 'link' : ''},
            {'description' : 'Midsummer day', 'date' : midsummer_day, 'link' : 'http://en.wikipedia.org/wiki/Midsummer'},
            {'description' : 'Father\'s day', 'date' : father_day, 'link' : 'http://en.wikipedia.org/wiki/Father%27s_Day'}]

def generate_json(years, output="years.json"):
    """ Generates the JSON for the specified years """

    days = []
    for year in years:
        DAYS_copy = copy.deepcopy(DAYS)
        for dictionary in DAYS_copy:
            for key, value in dictionary.items():
                if key == 'date':
                    dictionary[key] = convert_date_to_js(value, year)
        special = special_days(year)
        special_copy = copy.deepcopy(special)
        for dictionary in special_copy:
            for key, value in dictionary.items():
                if key == 'date':
                    dictionary[key] = convert_date_to_js(value, year)
        days.append(DAYS_copy+special_copy)
    
    with open(output, 'w') as outfile:
        json.dump(days, outfile)



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