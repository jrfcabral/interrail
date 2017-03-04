from pyquery import PyQuery as pq
from lxml import etree
import urllib
import sys
from datetime import datetime, timedelta
from itertools import repeat

def seconds_to_hours_mins(seconds):
    return int(seconds//3600), int((seconds//60)%60)

def parse_time(time):
    return datetime.strptime(time, '%I:%M %p').time()

def parse_item(item, day):
    required_symbols = {
        "Required": "☑",
        "": "☐",
        "Optional": "O"
    }
    departure_text = pq(item).find('div.time>span.departure-time').text()
    arrival_text = pq(item).find('div.time>span.arrival-time').text()
    departure_time = parse_time(departure_text)
    arrival_time = parse_time(arrival_text)
    departure = datetime.combine(day, departure_time)
    arrival_offset = 0 if departure_time < arrival_time else 1
    arrival = datetime.combine(day +  timedelta(days=arrival_offset), arrival_time)
    changes = pq(item).find('div.changes>span.text').text()
    reservation = required_symbols[pq(item).find('div.reservation>span.text').text()]
    hours, minutes = seconds_to_hours_mins((arrival-departure).total_seconds())
    duration_text = str(hours) + ":" + str(minutes)
    return departure.isoformat(sep=' ') + ', ' + arrival.isoformat(sep=' ') + ', ' + duration_text + ', ' + changes + ', '+ reservation

filename = sys.argv[1]
input = open(filename, "r").read()
d = pq(input, parser='html_fragments')
day = datetime.strptime(d("div.item-departure-date").eq(0).text(), '%A, %d.%m.%Y').date()
results = list(d("li.item_result>div.result"))


parsed_results =  list(map(parse_item, results, repeat(day)))
map(print, parsed_results)
with open(sys.argv[2], 'a+', encoding='utf-8') as csv_file:
    for line in parsed_results:
        csv_file.write(line+'\n')
    csv_file.close()
